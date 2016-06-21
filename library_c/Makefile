all:
	gcc -Wall -DTEST lib/blinkt.c -l bcm2835 -o blinkt

devel:
	-rm -r build
	python setup.py build
	sudo python setup.py develop
