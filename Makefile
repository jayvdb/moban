all: test

install:
	pip install .

install_test:
	pip install -r tests/requirements.txt

update:
	moban -m mobanfile
	git diff --exit-code

test:
	bash test.sh

lint:
	flake8 --max-line-length=88 --exclude=./.moban.d/setup.py,./docs/conf.py --ignore=W503,W504

format:
	isort -y $(find moban -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
	black -l 79 moban
	black -l 79 tests
