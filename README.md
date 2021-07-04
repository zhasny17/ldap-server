# ldap-server
The following project consists in a Restful API written in Python3, Flask and Python-ldap for CRUD operations in a LDAP server.


## `Requirements`
The project has been developed with the following stacks:
- Python 3.7
- Docker 20.10.7

## `API Setup`
First of all, make sure you have docker running on your development environment and on root directory of this project run the docker-compose file:
```
docker-compose up --build
```
This command will create instances of our REST API server, LDAP server and an admin interface.
- The API will be available on: http://localhost:5000/
- Being able to access the documentation interface at: http://localhost:5000/doc/
- And admin interface for ldap server hosted at: http://localhost:8090/ with login DN equals to *cn=admin,dc=techinterview,dc=com* and password *123456*

## `Unit tests`
Preferably within a virtual environment, being able to be created with venv python module:
```
python -m venv venv
```
Install packages on *requirements-dev.txt* with the command below:
```
pip install -r requirements-dev.txt
```
And just simplely run the pytest command on root directory of the project:
```
pytest
```
Using *pytest-docker* to help on integration tests with docker and docker-compose, we will be able to build all our infrastructure, run tests specified on *tests/user_test.py* and after that tear down everything.