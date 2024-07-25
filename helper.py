import os

def deep_get(data, keys):
    """
    Safely get a value from a nested dictionary or list.

    Parameters:
    - data: The dictionary or list to traverse.
    - keys: A list of keys/indexes to traverse.

    Returns:
    - The value if found, otherwise None.
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list) and isinstance(key, int) and key < len(data):
            data = data[key]
        else:
            return None
        if data is None:
            return None
    return data


def load_env_file():
    filepath = '.env'
    with open(filepath) as f:
        for line in f:
            # Remove any leading/trailing whitespace
            line = line.strip()
            # Ignore lines that are comments or are empty
            if not line or line.startswith('#'):
                continue
            # Split the line into key and value
            key, value = line.split('=', 1)
            # Set the environment variable
            os.environ[key] = value