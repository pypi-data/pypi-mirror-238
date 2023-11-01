PACKAGEVERSION="`python3 setup.py --version`"

all: test build-docs

test: update-test-data
	python3 -m unittest discover -s tests

build-docs:
	mkdocs build -d ../../python/$(PACKAGEVERSION)
	./update-doc-versions.sh

serve-docs:
	mkdocs serve

coverage: update-test-data
	python3-coverage run --branch -m unittest discover -s tests
	python3-coverage html

update-test-data:
	rsync ../../tests/samples.bin ../../tests/samples.pr tests

tag:
	git tag python-preserves@$(PACKAGEVERSION)

clean:
	rm -rf htmlcov
	find . -iname __pycache__ -o -iname '*.pyc' | xargs rm -rf
	rm -f .coverage
	rm -rf preserves.egg-info build dist

#
# sudo apt install python3-wheel twine
#
publish: clean build
	twine upload dist/*

build: build-docs
	python3 setup.py sdist bdist_wheel
