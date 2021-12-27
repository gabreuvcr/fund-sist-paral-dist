all: build

build: mandel-tiles-graphic.cpp
	g++ -o prog mandel-tiles-graphic.cpp -lgraph -lpthread -lm

run: build
	./prog $(ARGS)

clean: 
	/bin/rm -f *.o prog
