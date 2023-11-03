
def remove_key_recursive(d: dict, remove_key: str) -> dict:
    if not isinstance(d, dict):
        return d
    return {
        k: remove_key_recursive(v, remove_key)
        for k, v in d.items() if k != remove_key
    }