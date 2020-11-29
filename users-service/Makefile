.PHONY: all clean deps test run

venv:
	python -m venv venv

clean:
	rm -r venv

deps: venv
	source venv/bin/activate && \
	pip install \
		connexion \
		requests \
		pytest

test: venv
	source venv/bin/activate && \
	python -m users_service.test

run: venv
	source venv/bin/activate && \
	python -m users_service
