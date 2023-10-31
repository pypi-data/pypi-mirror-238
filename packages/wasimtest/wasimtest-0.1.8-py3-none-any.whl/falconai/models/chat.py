from falconai.config import config
from falconai.core.requests import request_endpoint

def chat(**kwargs):
    result = request_endpoint("chat", **kwargs)
    return result
