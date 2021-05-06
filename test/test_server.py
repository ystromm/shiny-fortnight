import pytest
from sanic_testing import TestManager

from server import server


def test_index_returns_200():
    server_under_test = server()
    TestManager(server_under_test)
    request, response = server_under_test.test_client.get('/healthcheck')
    assert response.status == 200
