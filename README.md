# jose-assignment



[![Build Status](https://github.com/jlopex/jose-assignment/workflows/TestCI/badge.svg)](https://github.com/jlopex/jose-assignment/actions)
[![Python 3.6](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

## INTRODUCTION

This project (a bit overengineered), implements what was requested in the exercise, using a 
DDD - hexagonals architecture approach.


## Architecture

The project uses a DDD approach separating the domain (entities) from the infrastructure:

 * Domain (in domain/ folder), contains the 3 domain entities (Content, Device, ProtectionSystem), <br />
along with several other models used for DB Insertion.
 * Uses a Relational DB database
 * There is a Cryptographical Service (dummy one of my own) which encrypts / decrypts the payloads.

This `CryptoService` can be set as a presentation layer between the DB and the API.

The global architecture is that of a monolith. If the architecture were to be scaled, consider splitting the 
monolith (Microservices, Serverless -Lamddas-, or Structured Monolith).


## Tech stack

This is a typical stack using:

* FastAPI, a modern and fast webserver (using async whenever possible)
* SQLAlchemy, a very well known ORM
* SQLite, a simple fast db (test run this in memory)

## Requirements
This project requires a Python virtualenv with python 3.11+.
You can create one with `python -m venv venv`. Activate it and do `make install`  there.

## Running the project
Do `make run` from the repository root. A SQLite DB will be created. For simplicity, this project
does not use DB migrations (Alembic). Once run, browse http://localhost:8000/docs to get an OpenAPI
(Swagger) documented API to test directly from the browser.

### Populating the DB
It's possible to seed the DB with initial values with `make populate-db`.

### Implementation

The following endpoints have been implemented:

#### Content

* GET /api/contents/{id}  # Get Content
* DELETE /api/contents/{id}  # Delete a Content
* PUT /api/contents/{id}  # Update a Content
* POST /api/contents/  # Add Content
* GET /api/stream/contents/{id}  # Get Content

#### Device

* GET /api/devices/{id}   # Get Device Info
* DELETE /api/devices/{id}   # Delete a Device
* GET /api/devices/   # List Device Systems
* POST /api/devices/   # Create Device System

#### Protection Systems

* GET /api/protection-systems/{id}   # Get Protection System
* GET /api/protection-systems/   # List Protection Systems
* POST /api/protection-systems/   #Create Protection System


### Future Improvements

Some potential improvements could be:

* Add DELETE method for protection-systems (will require to enable CASCADE DELETION in the Device and Content ORM models.
* Add UNIQUE Constraint to the DB ORM Models to avoid inserting protection systems or devices with repeated names.
* Add user auth and validation.
* Dockerize this app and use PostGreSQL or MySQL instead of SQlite
* Add real migrations with Alembic
* Research the usage of Async SQLAlchemy
* Code linting: add ruff (or flake8 + black) and isort to de CI pipeline


## Testing
Running tests requires installing dev dependencies first. Install them with `make install-dev`.
Tests include some examples of Unit, Integration and End to End cases in their respective folders.

Run the tests with `make test`

### Test CI
There is a little Pipeline for testing PR using GitHub actions.
See [here](https://github.com/jlopex/jose-assignment/blob/cd533b077dd8d83d2779f0e1a2629cd48c677a94/.github/workflows/test_ci.yml)

There is NO CD (Deployment) for this app.

## Considerations and Technical decisions
For simplicity's sake, no real AES cryptography module has been used. Instead two simple routines of my
own do a little cryptography, XORing the encryption key characters on the payload. The `CryptoService`
service is in charge of this. It has two _drivers_, one for each protection system. The two drivers provided
do a slightly different encryption so selection the wrong method for decrypting a payload will return garbled
result. This is intended.

The Content Repository won't allow to save an unencrypted content in the DB, and will raise an exception.
So to store the content, this must be encrypted first. This is signaled by the `is_encrypted` attribute in
the Content entity model.
