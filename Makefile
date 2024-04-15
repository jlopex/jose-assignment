test:
	pytest tests --disable-warnings  --verbosity=1 --color=yes

install:
	pip install -Ur requirements.txt

install-dev: install
	pip install -Ur requirements-dev.txt

run:
	uvicorn src.main:app --reload
