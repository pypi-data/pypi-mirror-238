import httpx
from ..config import config

async def request_endpoint(endpoint_name, **kwargs):
    endpoint = config.get_endpoint_data(endpoint_name)
    if not endpoint:
        raise ValueError(f"No configuration found for endpoint: {endpoint_name}")

    method = endpoint['method']
    url = endpoint['url']
    headers = endpoint['headers']
    data = extract_fields(endpoint["fields"], **kwargs)

    # Use Python's dynamic function invocation with getattr
    async with httpx.AsyncClient() as client:
        if method == 'POST':
            response = await client.post(url, headers=headers, json=data)
        else:
            response = await client.get(url, headers=headers)


    return response.json()

def extract_fields(fields, **kwargs):
    data = {}
    for field, value in fields.items():
        if isinstance(value, dict):
            data[field] = extract_fields(value, **kwargs)
        else:
            data[field] = kwargs.get(field, None)
    return data

