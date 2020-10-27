all: bof

bof: bof.c Makefile
	gcc -fno-stack-protector -no-pie -g -S bof.c
	# gcc -g -S bof.c
	gcc -o bof bof.s

clean:
	rm -f bof
