// C implementation for mandelbrot set fractals using libgraph, a simple
// library similar to the old Turbo C graphics library.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <iostream>
#include <math.h>
#include <vector>
#include <queue>
using namespace std;

#define MAXX 640
#define MAXY 480
#define MAXITER 32768

int NUM_THREADS, MAX_QUEUE;
FILE* input; // descriptor for the list of tiles (cannot be stdin)
int color_pick = 5; // decide how to choose the color palette
pthread_mutex_t mutex_queue, mutex_computer;
pthread_cond_t cond_not_full, cond_full;

//estatisticas
int total_tasks = 0, find_empty_queue = 0;
vector<int> tasks_per_worker;
vector<double> times_per_task;
double total_time = 0;

queue<struct fractal_param_t*> tasks_queue;

// params for each call to the fractal function
typedef struct fractal_param_t {
	int left; int low;  // lower left corner in the screen
	int ires; int jres; // resolution in pixels of the area to compute
	double xmin; double ymin;   // lower left corner in domain (x,y)
	double xmax; double ymax;   // upper right corner in domain (x,y)
} fractal_param_t;

int input_params() { 
	int n;

	fractal_param_t* p = (fractal_param_t*)malloc(sizeof(fractal_param_t));
	n = fscanf(input,"%d %d %d %d", 
		&(p->left), &(p->low), &(p->ires), &(p->jres));
	if (n == EOF) return n;

	if (n != 4) {
		perror("fscanf(left,low,ires,jres)");
		exit(-1);
	}
	n = fscanf(input,"%lf %lf %lf %lf",
		&(p->xmin), &(p->ymin), &(p->xmax), &(p->ymax));
	if (n != 4) {
		perror("scanf(xmin,ymin,xmax,ymax)");
		exit(-1);
	}
	tasks_queue.push(p);
	return 8;
}

//Insere uma tarefa nula para indicar EOW
void empty_params() {
	fractal_param_t* p = (fractal_param_t*)malloc(sizeof(fractal_param_t));
	p->left = 0, p->low = 0, p->ires = 0, p->jres = 0;
	p->xmin = 0, p->ymin = 0, p->xmax = 0, p->ymax = 0;
	tasks_queue.push(p);
}

//Thread do Reader, alimenta a fila e espera ficar vazia
void *read_thread(void *params) {
	int n = 0;
	//Loop que apos preencher a fila com o tamanho maximo ou até EOF,
	//fica esperando um sinal de algum Worker caso o número de tarefas
	//na fila seja menor ou igual ao numero de trabalhadores, bloqueando
	//o mutex e preenche novamente até o seu maximo ou até que atinja o EOF.
	//Quando termina, cria uma tarefa nula preenchida com zeros, que serve
	//para informar EOW, finalizando sua execucao.
	while (1) {
		pthread_mutex_lock(&mutex_queue);
		//Depois de preencher, aguarda algum Worker notificar
		//que a fila esvaziou
		while (tasks_queue.size() >= MAX_QUEUE) {
			pthread_cond_wait(&cond_not_full, &mutex_queue);
		}
		//Preenche a fila até que atingir o maximo ou encontrar EOF
		while (tasks_queue.size() < MAX_QUEUE && n != EOF) {
			n = input_params();
		}
		//Caso for EOF, coloca uma tarefa EOW na fila
		if (n == EOF) empty_params();
	
		pthread_cond_broadcast(&cond_full);
		pthread_mutex_unlock(&mutex_queue);
		//Encerra a thread
		if (n == EOF) break;
	}
	pthread_exit(NULL);
}

//Verifica se a tarefa passada como parametro é EOW
int end_of_work(fractal_param_t* p) {
	return p->left == 0 && p->low == 0 && p->ires == 0 && p->jres == 0 &&
		   p->xmin == 0 && p->ymin == 0 && p->xmax == 0 && p->ymax == 0;
}

// Function to draw mandelbrot set
//Thread do Worker, consome as tarefas da fila até encontrar EOW
void *fractal_thread(void *params) {
	double dx, dy;
	int i, j, k, color;
	double x, y, u, v, u2, v2, time_task;
	long id = (long)params;
	struct timespec start, end;
	//Loop que inicia, após bloquear o mutex da fila, verificando se está vazia, que em caso positivo
	//espera até que o Reader mande um broadcast para dizer que já possui itens disponiveis.
	//Apos isso, o Worker retira uma tarefa da fila e checa se é EOW (atributos zerados, se for,
	//finaliza sua execucao) e entao checa se precisa enviar um signal para o Reader encher mais
	//a fila (ele nao manda signal se a ultima tarefa, last_p, for EOW). Por fim, libera o mutex
	//e realiza suas operacoes
	while (1) {

		pthread_mutex_lock(&mutex_queue);
		//Se estiver vazia, aguarda
		while (tasks_queue.empty()) {
			pthread_mutex_lock(&mutex_computer);
			find_empty_queue++; //incrementa contador de fila vazia
			pthread_mutex_unlock(&mutex_computer);
			pthread_cond_wait(&cond_full, &mutex_queue);
		}

		//Verifica se a proxima tarefa é EOW, caso seja verdade
		//encerra sua thread. Nao remove o item da fila
		fractal_param_t* p = tasks_queue.front();
		if (end_of_work(p)) {
			pthread_mutex_unlock(&mutex_queue);
			break;
		}
		//Se nao for EOW, retira a tarefa
		tasks_queue.pop();
		clock_gettime(CLOCK_REALTIME, &start);

		//Caso a fila esvaziou e a ultima tarefa não for EOW
		//entao avisa o Reader para preencher a fila
		fractal_param_t* last_p = tasks_queue.back();
		if (tasks_queue.size() <= NUM_THREADS && !end_of_work(last_p)) {
			pthread_cond_signal(&cond_not_full);
		}
		pthread_mutex_unlock(&mutex_queue);
		
		dx = (p->xmax - p->xmin) / p->ires;
		dy = (p->ymax - p->ymin) / p->jres;
		
		// scanning every point in that rectangular area.
		// Each point represents a Complex number (x + yi).
		// Iterate that complex number
		for (j = 0; j < p->jres; j++) {
			for (i = 0; i <= p->ires; i++) {
				x = i * dx + p->xmin; // c_real
				u = u2 = 0; // z_real
				y = j * dy + p->ymin; // c_imaginary
				v = v2 = 0; // z_imaginary

				// Calculate whether c(c_real + c_imaginary) belongs
				// to the Mandelbrot set or not and draw a pixel
				// at coordinates (i, j) accordingly
				// If you reach the Maximum number of iterations
				// and If the distance from the origin is
				// greater than 2 exit the loop
				for (k = 0; (k < MAXITER) && ((u2 + v2) < 4); ++k) {
					// Calculate Mandelbrot function
					// z = z*z + c where z is a complex number

					// imag = 2*z_real*z_imaginary + c_imaginary
					v = 2 * u * v + y;
					// real = z_real^2 - z_imaginary^2 + c_real
					u  = u2 - v2 + x;
					u2 = u * u;
					v2 = v * v;
				}
				if (k == MAXITER) {
					// converging areas are black
					color = 0;
				} else {
					// graphics mode has only 16 colors;
					// choose a range and recycle!
					color = ( k >> color_pick ) % 16;
				}
			}
		}
		clock_gettime(CLOCK_REALTIME, &end);
		pthread_mutex_lock(&mutex_computer);
		total_tasks++; //incrementa numero de tarefas
		tasks_per_worker[id]++; //incrementa o numero de tarefas da thread
		time_task =  1.e+3 * (double)(end.tv_sec - start.tv_sec);
		time_task += 1.e-6 * (double)(end.tv_nsec - start.tv_nsec);
		times_per_task.push_back(time_task); //armazena o tempo gasto para realizar a tarefa
		pthread_mutex_unlock(&mutex_computer);
		free(p);
	}
	pthread_exit(NULL);
}

double task_standard_deviation(double mean, vector<int> data) {
	double sd = 0;
	for (int i = 0; i < data.size(); i++) {
		sd += pow(data[i] - mean, 2);
	}
	return sqrt(sd / NUM_THREADS);
}

double time_standard_deviation(double mean, vector<double> data) {
	double sd = 0;
	for (int i = 0; i < data.size(); i++) {
		sd += pow(data[i] - mean, 2);
	}
	return sqrt(sd / data.size());
}

void compute_statistics() {
	double avg_tasks_pw = 0, sd_tasks_pw = 0;
	double avg_time = 0, sd_time = 0;

	avg_tasks_pw = (double)total_tasks / NUM_THREADS;
	sd_tasks_pw = task_standard_deviation(avg_tasks_pw, tasks_per_worker);
	
	double total_time = 0;
	for (int i = 0; i < times_per_task.size(); i++) {
		total_time += times_per_task[i];
	}
	avg_time = total_time / times_per_task.size();
	sd_time = time_standard_deviation(avg_time, times_per_task);

	printf("Tarefas: total = %d;  média por trabalhador = %f(%f)\n", total_tasks, avg_tasks_pw, sd_tasks_pw);
	printf("Tempo médio por tarefa: %.6f (%.6f) ms\n", avg_time, sd_time);
	printf("Fila estava vazia: %d vezes\n", find_empty_queue);
}

int main (int argc, char* argv[]) {
	int i, j, k, rc;
	fractal_param_t p;
	pthread_t reader, computer;

	if ((argc != 2) && (argc != 3)) {
		fprintf(stderr,"usage %s filename [color_pick]\n", argv[0] );
		exit(-1);
	} 

	//Define o numero de threads, se nao for passado
	//argumento, utiliza por padrao 4
	if (argc == 3) {
		NUM_THREADS = atoi(argv[2]);
	} else {
		NUM_THREADS = 4;
	}

	MAX_QUEUE = NUM_THREADS * 4;

	if ((input = fopen(argv[1],"r")) == NULL) {
		perror("fdopen");
		exit(-1);
	}

	pthread_t workers[NUM_THREADS];
	
	//Preenche as primeiras NUM_THREADS posicoes do vector com 0
	tasks_per_worker.assign(NUM_THREADS, 0);

	pthread_mutex_init(&mutex_queue, NULL);
	pthread_mutex_init(&mutex_computer, NULL);
	pthread_cond_init(&cond_not_full, NULL);
	pthread_cond_init(&cond_full, NULL);

	rc = pthread_create(&reader, NULL, read_thread, NULL);
	if (rc) exit(-1);

	for (long t = 0; t < NUM_THREADS; t++) {
		rc = pthread_create(&workers[t], NULL, fractal_thread, (void *) t);
		if (rc) exit(-1);
	}

	for(long t = 0; t < NUM_THREADS; t++) {
		pthread_join(workers[t], NULL);
	}

	pthread_join(reader, NULL);
	
	pthread_cond_destroy(&cond_not_full);
	pthread_cond_destroy(&cond_full);
	pthread_mutex_destroy(&mutex_queue);
	pthread_mutex_destroy(&mutex_computer);

	tasks_queue.pop(); //Remove o EOW, ultimo item da fila

	compute_statistics();

	return 0;
}
