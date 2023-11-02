import re

class ConfigManager:
    def __init__(self, config):
        self.config = config

    def _get_target(self, key_str):
        keys_split = key_str.lower().split('.')
        target = self.config
        for key in keys_split[:-1]:
            target = target.setdefault(key, {})
        return target, keys_split[-1]

    def update(self, key_str, value):
        target, last_key = self._get_target(key_str)
        target[last_key] = value

    def push(self, key_str, value):
        target, last_key = self._get_target(key_str)
        target[last_key].append(value)

    def delete(self, key_str):
        target, last_key = self._get_target(key_str)
        if last_key in target:
            del target[last_key]

    def insert(self, key_str, index, value):
        target, last_key = self._get_target(key_str)
        target[last_key].insert(index, value)

    def pop(self, key_str, index=-1):
        target, last_key = self._get_target(key_str)
        return target[last_key].pop(index)

    def get(self, key_str, default=None):
        try:
            target, last_key = self._get_target(key_str)
            return target.get(last_key, default)
        except Exception:
            return default

        
    def interpolate_values(self, data, reference=None):
        """
        Recursively traverse the given data and resolve placeholders with 
        their corresponding values from the reference.
        """
        if reference is None:
            reference = self.config

        # Generate an enhanced reference without modifying the original
        enhanced_ref = {**reference}
        for key, value in reference.items():
            if key.islower():
                enhanced_ref[key.upper()] = value
            elif key.isupper():
                enhanced_ref[key.lower()] = value

        interpolated = {}
        for key, value in data.items():
            if isinstance(value, str) and "{" in value:
                try:
                    interpolated[key] = value.format(**enhanced_ref)
                except KeyError:
                    interpolated[key] = value  # Leave the original value if interpolation fails
            elif isinstance(value, dict):
                interpolated[key] = self.interpolate_values(value, enhanced_ref)
            else:
                interpolated[key] = value
        return interpolated

    
    def interpolate_values2(self, value, reference=None):
        """
        Interpolates values based on the format `{{key.subkey.subsubkey...}}`.
        """
        if reference is None:
            reference = self.config

        def replacer(match):
            keys = match.group(1).split('.')
            result = reference
            for key in keys:
                result = result.get(key)
                if result is None:
                    return match.group(0)
            return str(result)

        return re.sub(r"{{([\w\.]+)}}", replacer, value)



# # Example usage:
# config = {
#     "list_attr": [1, 2, 3],
#     "nested": {
#         "attr": "value",
#         "another_list": ["a", "b", "c"]
#     }
# }

# manager = ConfigManager(config)

# # Update
# manager.update("nested.attr", "new_value")
# print(config)

# # Push/Add
# manager.push("list_attr", 4)
# print(config)

# # Delete
# manager.delete("nested.attr")
# print(config)

# # Insert
# manager.insert("nested.another_list", 1, "z")
# print(config)

# # Pop
# popped_item = manager.pop("nested.another_list", 1)
# print(popped_item)
# print(config)

# # Get
# print(manager.get("nested.another_list"))
