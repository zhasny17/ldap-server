import os
import pytest
import requests
from requests.exceptions import ConnectionError


#############################################################################
#                              HELP FUNCTIONS                               #
#############################################################################
def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    port = docker_services.port_for("app", 5000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


#############################################################################
#                             HAPPY PATH TESTS                              #
#############################################################################
def test_add_user(http_service):
    response = requests.post(
        http_service + "/users",
        json={
            "uid": "56789",
            "cn": "Marcos",
            "sn": "Marcos"
        }
    )

    assert response.status_code == 201


def test_get_user(http_service):
    response = requests.get(
        http_service + "/users/56789",
    )

    assert response.status_code == 200


def test_get_users(http_service):
    response = requests.get(
        http_service + "/users",
    )

    assert response.status_code == 200
    data = response.json()
    users = data['users']
    assert len(users) > 0


#############################################################################
#                          NO HAPPY PATH TESTS                              #
#############################################################################
def test_add_user_with_property_error(http_service):
    response = requests.post(
        http_service + "/users",
        json={
            "uid": "56789",
            "cn": 123,
            "sn": "Marcos"
        }
    )

    assert response.status_code == 400


def test_add_user_with_no_required_property(http_service):
    response = requests.post(
        http_service + "/users",
        json={
            "uid": "56789",
            "sn": "Marcos"
        }
    )

    assert response.status_code == 400


def test_add_user_with_conflict_error(http_service):
    data = {
        "uid": "123",
        "cn": "Lucas",
        "sn": "Luz"
    }
    response = requests.post(
        http_service + "/users",
        json=data
    )
    assert response.status_code == 201

    response = requests.post(
        http_service + "/users",
        json=data
    )
    assert response.status_code == 409


def test_get_nonexistent_user(http_service):
    response = requests.get(
        http_service + "/users/1111",
    )

    assert response.status_code == 404