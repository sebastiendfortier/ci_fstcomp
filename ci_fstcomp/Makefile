# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m fstcompstats fstcompstats.f90

interface:
	f2py3 --overwrite-signature -h fstcompstats.pyf fstcompstats.f90 -m fstcompstats

clean:
	rm -f *.pyf *.so
