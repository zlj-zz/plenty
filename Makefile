Project = plenty
PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.7")' && \
	      which python3) )

ifeq ($(PY),)
  $(error No suitable python found(>=3.8).)
endif

test:
	@if [ ! -f pytest ]; then $(PY) -m pip install pytest; fi
	pytest ./tests
	# pytest ./tests --cov=pigit --cov-report=html

run:
	$(PY) ./tests/test_run.py

lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 -v --ignore=W503,F403,F405,E501,E402,E203,E741,E401 --show-source ./$(Project)
	@echo

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

del:
	@if [ -d ./dist ]; then rm -r ./dist/; fi
	@if [ -d ./build ]; then rm -r ./build; fi
	@if [ -d ./$(Project).egg-info ]; then rm -r "./$(Project).egg-info"; fi

release: del clean
	$(PY) setup.py sdist bdist_wheel
	twine upload dist/*

install: del clean
	$(PY) -m pip uninstall pigit
	$(PY) setup.py install

todo:
	@grep --color -Ion '\(TODO\|XXX\|FIXME\).*' -r $(Project)

uml:
	pyreverse -ASmy -o png $(Project) -d docs

.PHONY: run lint clean del install release todo test uml
