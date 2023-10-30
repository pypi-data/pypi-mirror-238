import requests
from falconai import config

def chat(query, model_type, app_type, plugin_ids, is_regenerate=True):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.API_KEY}'
    }

    data = {
        "query": query,
        "model_type": model_type,
        "app_type": app_type,
        "plugin_ids": plugin_ids,
        "is_regenerate": is_regenerate
    }

    response = requests.post(f"{config.BASE_URL}/api/v1/chat", headers=headers, json=data)
    return response.json()
