
test:
	python setup.py test

install:
	python setup.py install

clean:
	rm -rf *.egg-info
	rm -rf build
	find . -name \*.pyc | xargs rm -f

realclean:	clean
	rm -rf dist
	find . -name \*~ | xargs rm -f
	find . -name \*.so | xargs rm -f

