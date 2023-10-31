from tenacity import retry, stop_after_attempt, wait_random_exponential

httpx_client: tuple = None, None


def get_client():
    import httpx
    from datetime import datetime, timedelta
    global httpx_client
    now = datetime.utcnow()
    if httpx_client[0] is None or httpx_client[1] < (now - timedelta(hours=1)):
        httpx_client = httpx.AsyncClient(http2=True, follow_redirects=True), now
    return httpx_client[0]


def format_async_response_body(response):
    js = dict()
    try:
        js = response.json()
    except ValueError:
        js['content'] = response.text
    return js


async def safe_json_request(method, url, stop=stop_after_attempt(3), reraise=True,
                            wait=wait_random_exponential(multiplier=.01, max=1), **kwargs):
    import httpx
    @retry(stop=stop, reraise=reraise, wait=wait)
    async def make_async_request():
        resp = await get_client().request(method=method, url=url, **kwargs)
        status = resp.status_code
        js = format_async_response_body(response=resp)
        if status >= 500:
            resp.raise_for_status()
        return status, js

    try:
        status_code, js = await make_async_request()
    except httpx.RequestError:
        status_code, js = None, dict()
    except httpx.HTTPStatusError as e:
        js = format_async_response_body(response=e.response)
        status_code = e.response.status_code
    return status_code, js


def generate_oauth_headers(access_token: str) -> dict:
    """Convenience function to generate oauth stand authorization header

    :param access_token: Oauth access token
    :return: Request headers
    """
    return {'Authorization': 'Bearer ' + access_token}
