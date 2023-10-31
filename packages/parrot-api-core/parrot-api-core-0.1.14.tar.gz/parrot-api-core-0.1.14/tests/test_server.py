import pytest


@pytest.fixture()
def client(test_directory):
    import os
    from parrot_api.core.server import create_server
    app = create_server(spec_dir=os.path.join(test_directory, 'mocks/example_app/schemas'))
    return app.app.tpest_client()


def test_package_apis(test_directory):
    from parrot_api.core.server import create_server
    import os
    import shutil
    new_package_dir = os.path.join(test_directory, '../parrot_api/example_package')
    if os.path.isdir(new_package_dir):
        shutil.rmtree(new_package_dir)
    shutil.copytree(os.path.join(test_directory, 'mocks/example_package/'), new_package_dir)
    client = create_server(
        spec_dir=os.path.join(test_directory, os.path.join(test_directory, 'mocks/example_app/schemas')),

    ).test_client()
    js = dict(head=1)
    assert client.post('/package/v1/echo', json=js).json() == js
    shutil.rmtree(new_package_dir)


@pytest.fixture()
def client(test_directory):
    import os
    from parrot_api.core.server import create_server
    app = create_server(spec_dir=os.path.join(test_directory, 'mocks/async_app/schemas'))
    return app.test_client()


async def test_async_template_home(client):
    resp = client.get('/status/v1/healthcheck')
    assert resp.status_code == 200


async def test_async_template_api_ui(client):
    resp = client.get('v1/ui/')
    assert resp.status_code == 200


async def test_async_hello(client):
    resp = client.get('/v1/hello', headers=dict(Authorization='Bearer test'))
    assert resp.status_code == 200
