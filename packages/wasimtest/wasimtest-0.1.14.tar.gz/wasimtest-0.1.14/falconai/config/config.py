import json
import os
from ..utils.config_manager import ConfigManager

class FalconConfig:
    def __init__(self, config_path_or_file="config.json"):
        # If the provided path is not absolute, assume it's a filename relative to this script's directory
        if not os.path.isabs(config_path_or_file):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            config_path = os.path.join(dir_path, config_path_or_file)
        else:
            config_path = config_path_or_file
        self._load_config(config_path)
        self._update_config_with_env_vars()

    def _load_config(self, config_path):
        # Load the config file
        with open(config_path, "r") as f:
            CONFIG = json.load(f)
            # Convert all keys to lowercase
            lowercased_config = self._recursive_key_lowercase(CONFIG)
            self.config = ConfigManager(lowercased_config)
    
    def _recursive_key_lowercase(self, data):
        """Recursively convert dictionary keys to lowercase."""
        if isinstance(data, dict):
            return {k.lower(): self._recursive_key_lowercase(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._recursive_key_lowercase(item) for item in data]
        else:
            return data


    def _update_config_with_env_vars(self):
        # Iterate over environment variables
        for key, value in os.environ.items():
            # Convert key to lowercase
            key = key.lower()
            if key.startswith('falcon_'):
                # Removing the FALCON_ prefix to match with the config key
                config_key = key.replace('falcon_', '')
                if config_key in self.config.config:
                    self.config.update(config_key, value)
            elif key in self.config.config:
                self.config.update(key, value)

    def get_base_url(self):
        return self.config.get("base_url", default="http://localhost:8000")

    def get_api_key(self):
        return self.config.get("api_key")

    def get_chat_url(self):
        return self.config.get("endpoints.chat.url", default="")  # Example to retrieve chat URL
    
    def get_endpoint(self, endpointName):
        return self.config.get(f"endpoints.{endpointName}")
    
    def get_endpoint_data(self, endpointName):
        base_url = self.config.get("base_url")
        endpoint_config = self.get_endpoint(endpointName)

        # Determine URL
        if "url" in endpoint_config:
            endpoint_url = endpoint_config["url"]
        else:
            endpoint_url = f"{base_url}/{endpoint_config.get('path', '')}"

        # Determine headers
        common_headers = self.config.get("headers", {})
        endpoint_headers = endpoint_config.get("headers", {})
        final_headers = {**common_headers, **endpoint_headers}
        # Interpolate the headers
        final_headers = self.config.interpolate_values(final_headers)

        # Extract fields
        data_fields = self._extract_fields(endpoint_config.get("fields", {}))

        # Prepare the results
        result = {
            "url": endpoint_url,
            "headers": final_headers,
            "fields": data_fields
        }

        # Add remaining attributes from endpoint_config
        for key, value in endpoint_config.items():
            if key not in result:
                result[key] = value

        return result

    def _extract_fields(self, fields_config):
        """Extract fields and their types from the configuration."""
        fields = {}
        for key, value in fields_config.items():
            if isinstance(value, dict):
                fields[key] = self._extract_fields(value)
            else:
                fields[key] = value
        return fields

    def override_config(self, path, value):
        self.config.update(path, value)

    def add_to_config(self, path, value):
        # Assuming you have an `add` method in your ConfigManager
        self.config.add(path, value)

    def delete_from_config(self, path):
        # Assuming you have a `delete` method in your ConfigManager
        self.config.delete(path)

    def push_to_config_array(self, path, value):
        # Assuming you have a `push` method in your ConfigManager
        self.config.push(path, value)

    def pop_from_config_array(self, path):
        # Assuming you have a `pop` method in your ConfigManager
        self.config.pop(path)
