import io
from unittest.mock import MagicMock, ANY

import pytest
from sanic_testing import TestManager

from server import server


def test_get_healtcheck_returns_200():
    server_under_test, _ = server_factory()
    TestManager(server_under_test)
    request, response = server_under_test.test_client.get('/healthcheck')
    assert response.status == 200


def test_get_schema_returns_empty_list():
    server_under_test, _ = server_factory()
    request, response = server_under_test.test_client.get('/schema')
    assert response.status == 200
    assert response.json == []


def test_get_schema_should_list_objects():
    server_under_test, s3 = server_factory()
    s3.list_objects_v2.return_value = {
        'Contents': [
            {
                'Key': 'a.json'
            },
            {
                'Key': 'b.json'
            }
        ]
    }
    request, response = server_under_test.test_client.get('/schema')
    s3.list_objects_v2.assert_called_with(bucket="schema_prod")
    assert response.status == 200
    assert response.json == ["a", "b"]


def test_get_schema_should_download_fileobj():
    server_under_test, s3 = server_factory()
    s3.get_object.return_value = {"Body": io.BytesIO('{"a": "a"}'.encode())}
    request, response = server_under_test.test_client.get('/schema/a')
    s3.get_object.assert_called_with(Bucket="schema_prod", Key="a.json")
    assert response.status == 200
    assert response.json == {"a": "a"}

def test_get_schema_should_upload_fileobj():
    server_under_test, s3 = server_factory()
    request, response = server_under_test.test_client.post('/schema/a', json={"a": "a"})
    s3.upload_fileobj.assert_called_with(ANY, Bucket="schema_prod", Key="a.json")
    assert response.status == 201

def server_factory():
    s3 = MagicMock()
    server_under_test = server(s3)
    TestManager(server_under_test)
    return server_under_test, s3
