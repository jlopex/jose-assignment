# jose-assignment



[![Build Status](https://github.com/jlopex/jose-assignment/workflows/TestCI/badge.svg)](https://github.com/jlopex/jose-assignment/actions)


## INTRODUCTION

This project (a bit overengineered), implements what was requested in the exercise, using a 
DDD - hexagonals architecture approach.


## Architecture

The project uses a DDD approach separating the domain (entities) from the infrastructure:

 * Domain (in domain/ folder), contains the 3 domain entities (Content, Device, ProtectionSystem), <br />
along with several other models used for DB Insertion.


## Tech stack

This is a typical stack using:

* FastAPI, a modern and fast webserver (using async whenever possible)
* SQLAlchemy, a very well known ORM
* SQLite, a simple fast db (test run this in memory)

## Requirements
This project requires a Python virtualenv with python 3.11+.
You can create one with `python -m venv venv`. Activate it and do `make install`  there.

### Running the project
Do `make run` from the repository root. A SQLite DB will be created. For simplicity, this project
does not use DB migrations (Alembic).


## Testing

Runing tests requires installing dev dependencies first. Install them with `make install-dev`.
Run the tests with `make test`
