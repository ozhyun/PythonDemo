##
#
#

all: libapi.so

libapi.so: api.o
	gcc -shared -fPIC -o $@ $^

%.o : %.c
	gcc -fPIC -c $^


clean:
	rm -f *.o libapi.so
