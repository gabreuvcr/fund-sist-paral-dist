#include <stdlib.h>
#include <stdio.h>
#include "queue.h"

queue_t* create_queue() {
    queue_t* queue = (queue_t*)malloc(sizeof(queue_t));
    queue->first = NULL;
    queue->end = NULL;
    queue->length = 0;
    queue->max = 4 * NUM_THREADS;
    return queue;
}

void free_queue(queue_t* queue) {
    fractal_param_t* current = queue->first;
    while (current != NULL) {
        fractal_param_t* aux = current->next;
        free(current);
        current = aux;
    }
    free(queue);
}

int empty_queue(queue_t* queue) {
    return queue->first == NULL;
}

void push_queue(queue_t* queue, fractal_param_t* new_fractal) {
    if (queue->length >= queue->max) {
        return;
    }

    new_fractal->next = NULL;

    if (empty_queue(queue) == 1) {
        queue->first = new_fractal;
        queue->end = new_fractal;
    } else {
        queue->end->next = new_fractal;
        queue->end = new_fractal;
    }
    queue->length++;
}

fractal_param_t* pop_queue(queue_t* queue) {
    if (empty_queue(queue) == 1) {
        return NULL;
    }

    fractal_param_t* removed = queue->first;
    queue->first = queue->first->next;
    queue->length--;

    return removed;
}
