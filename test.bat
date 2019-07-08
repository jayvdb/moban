pip freeze

nosetests --with-coverage --cover-package=moban --cover-package=tests

flake8 --max-line-length=88 --exclude=docs,.moban.d --ignore=W503,W504
