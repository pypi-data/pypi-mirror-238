def create_server(spec_dir, additional_middleware: list = None, debug=False):
    from connexion import AsyncApp, ConnexionMiddleware
    import os
    import orjson
    import yaml
    from parrot_api.core.common import get_subpackage_paths

    middleware_stack = ConnexionMiddleware.default_middlewares + additional_middleware if additional_middleware else ConnexionMiddleware.default_middlewares

    app = AsyncApp(__name__, middlewares=middleware_stack, jsonifier=orjson)
    for spec in os.listdir(spec_dir):
        app.add_api(specification=os.path.join(spec_dir, spec), validate_responses=debug)

    for path in get_subpackage_paths():
        schema_directory = os.path.join(path, 'schemas/')
        if os.path.isdir(schema_directory):
            for spec_file in [i for i in os.listdir(schema_directory) if i.endswith('yaml') or i.endswith("yml")]:
                with open(os.path.join(schema_directory, spec_file), 'rt') as f:
                    spec = yaml.safe_load(f)
                app.add_api(specification=spec, validate_responses=debug)
    return app


async def healthcheck():
    return dict(status='ok')

async def hello():
    return dict(status='ok')
