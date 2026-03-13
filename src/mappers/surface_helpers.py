from collections.abc import Mapping


def flatten_dict(obj: Mapping, prefix: str = "", sep: str = ".") -> dict[str, object]:
    flat: dict[str, object] = {}
    for key, value in obj.items():
        full_key = f"{prefix}{sep}{key}" if prefix else str(key)
        if isinstance(value, Mapping):
            flat.update(flatten_dict(value, prefix=full_key, sep=sep))
        else:
            flat[full_key] = value
    return flat
