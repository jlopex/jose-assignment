test:
	pytest tests --disable-warnings

install:
	pip install -Ur requirements.txt

install-dev: install
	pip install -Ur requirements-dev.txt
