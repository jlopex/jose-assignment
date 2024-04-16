help:  # Shows a help text
	@echo 'Type make <command> to manage the project.'
	@echo 'Available commands:'
	@echo " "
	@grep -e '^[a-zA-Z]' Makefile | sed -e "s/:[^#]*#/%/" | column -t -s$$%

test:  # Run tests
	pytest tests --disable-warnings  --verbosity=1 --color=yes

install:  # Install dependencies
	pip install -Ur requirements.txt

install-dev: install  # Installs development dependencies
	pip install -Ur requirements-dev.txt

run:  # Runs the server. Browse on http://localhost:8000/docs
	uvicorn src.main:app --reload

migration:  # Execute DB Migrations
	# Currently we won't use alembic. Just DB initialization
	python -m src.main

populate-db:  # Populate the DB with initial values (does migration)
	PYTHONPATH=. python src/tools/seed_db.py
