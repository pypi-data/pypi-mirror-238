import json

import httpx
import pytest


@pytest.fixture()
def async_client(test_directory):
    import os
    from parrot_api.core.server import create_server
    app = create_server(spec_dir=os.path.join(test_directory, 'mocks/schemas'))
    return app.test_client()


def test_valid_token(async_client, respx_mock, valid_access_headers, public_keys, app_settings):
    respx_mock.get(url=app_settings['auth_keys_url']).side_effect = httpx.Response(200, json=public_keys)
    resp = async_client.get('/v1/hello', headers=valid_access_headers)
    assert resp.status_code == 200


async def test_invalid_token(async_client, respx_mock, invalid_access_headers, public_keys, app_settings):
    respx_mock.get(url=app_settings['auth_keys_url']).side_effect = httpx.Response(200, json=public_keys)
    resp = async_client.get('/v1/hello', headers=invalid_access_headers)
    assert resp.status_code == 401


async def test_unauthorized_token(async_client, respx_mock, unauthorized_access_headers, public_keys,
                                  app_settings):
    respx_mock.get(url=app_settings['auth_keys_url']).side_effect = httpx.Response(200, json=public_keys)
    resp = async_client.get('/v1/hello', headers=unauthorized_access_headers)
    assert resp.status_code == 403
