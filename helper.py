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