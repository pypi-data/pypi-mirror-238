from falconai.core.requests import request_endpoint

def chat(**kwargs):
    result = request_endpoint("chat", **kwargs)
    return result

def plugin_chat(**kwargs):
    result = request_endpoint("plugin_chat", **kwargs)
    return result
