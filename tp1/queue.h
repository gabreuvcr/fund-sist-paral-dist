#ifndef QUEUE_H
#define QUEUE_H

#define NUM_THREADS 5

// params for each call to the fractal function
typedef struct fractal_param_t {
	int left; int low;  // lower left corner in the screen
	int ires; int jres; // resolution in pixels of the area to compute
	double xmin; double ymin;   // lower left corner in domain (x,y)
	double xmax; double ymax;   // upper right corner in domain (x,y)
	struct fractal_param_t *next;
} fractal_param_t;

typedef struct queue_t {
    fractal_param_t* first;
    fractal_param_t* end;
    int length;
    int max;
} queue_t;

queue_t* create_queue();
void free_queue(queue_t* queue);
int empty_queue(queue_t* queue);
void push_queue(queue_t* queue, fractal_param_t* new_fractal);
fractal_param_t* pop_queue(queue_t* queue);

#endif
