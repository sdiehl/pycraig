TARGET  := jellyfish.so
SRC    := damerau_levenshtein.c jaro.c levenshtein.c mra.c porter.c hamming.c              jellyfishmodule.c  metaphone.c    nysiis.c  soundex.c
OBJS   := ${SRC:.c=.o} 

PYTHONPATH = /usr/include/python2.6

CCFLAGS = -O3 -Wall -fPIC -I$(PYTHONPATH)
LDFLAGS = -shared
LIBS    = 

.PHONY: all clean distclean 
all:: ${TARGET} 

${TARGET}: ${OBJS} 
	${CC} ${LDFLAGS} -o $@ $^ ${LIBS} 

${OBJS}: %.o: %.c ${SRC}
	${CC} ${CCFLAGS} -o $@ -c $< 

clean:
	-rm -f *~ ${OBJS} ${TARGET}

distclean:: clean
