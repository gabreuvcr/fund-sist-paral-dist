import sys

def input_text(file):
    first = 1
    last = 9
    for i in range(first, last):
        raw_file = file.replace(".in", "")
        text = f"./prog ./mandelbrot_tasks/{file} {i} >> {raw_file}.out"
        print(text, end=' && ' if i < last - 1 else "\n")

file = sys.argv[1];
input_text(file)
