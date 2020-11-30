venv:
	python -m venv venv

fb-init: venv
	source venv/bin/activate && \
	curl -sL firebase.tools | bash && \
	firebase init

deps: venv
	source venv/bin/activate && \
	python -m pip install -r requirements.txt

run: venv
	source venv/bin/activate && \
	python -m calendarApi

fb-emulator:
	firebase emulators:start

test: venv
	source venv/bin/activate && \
	pytest -s -vv

clean:
	rm -r venv