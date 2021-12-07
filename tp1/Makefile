all: build

build: mandel-tiles-graphic.cpp
	g++ -c queue.c
	g++ -o prog mandel-tiles-graphic.cpp queue.o -lgraph -lpthread -lm

run: build
	./prog $(ARGS)

clean: 
	/bin/rm -f *.o prog
