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
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "", "docker-compose.yml")

@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("app", 5000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url





#############################################################################
#                             HAPPY PATH TESTS                              #
#############################################################################
def test_status_code(http_service):
    status = 200
    response = requests.get(http_service + "/")

    assert response.status_code == status


#############################################################################
#                          NO HAPPY PATH TESTS                              #
#############################################################################