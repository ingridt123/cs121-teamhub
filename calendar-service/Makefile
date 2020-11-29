venv:
	python -m venv venv

deps: venv
	source venv/bin/activate && \
	python -m pip install -r requirements.txt

run: venv
	source venv/bin/activate && \
	python -m calendarApi

test: venv
	source venv/bin/activate && \
	pytest -s -vv

clean:
	rm -r venv