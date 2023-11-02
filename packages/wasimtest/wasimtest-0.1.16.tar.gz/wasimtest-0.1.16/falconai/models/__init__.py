from ..core.requests import request_endpoint

async def chat(**kwargs):
    result = await request_endpoint("chat", **kwargs)
    return result