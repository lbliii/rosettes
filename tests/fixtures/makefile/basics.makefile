CC = gcc
CFLAGS = -Wall -g

all: program

program: main.o utils.o
	$(CC) $(CFLAGS) -o program main.o utils.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

clean:
	rm -f *.o program

.PHONY: all clean