from collections.abc import Mapping


def flatten_dict(obj: Mapping, prefix: str = "", sep: str = "_") -> dict[str, object]:
    flat: dict[str, object] = {}
    for key, value in obj.items():
        full_key = f"{prefix}{sep}{key}" if prefix else str(key)
        if isinstance(value, Mapping):
            flat.update(flatten_dict(value, prefix=full_key, sep=sep))
        else:
            flat[full_key] = value
    return flat


def normalize_surfacegrid_payload(payload: dict) -> dict:
    normalized = dict(payload)

    rotation_i = normalized.get("rotation_i")
    if rotation_i is not None:
        normalized["rotation_i"] = round(float(rotation_i), 4)

    rotation_j = normalized.get("rotation_j")
    if rotation_j is not None:
        normalized["rotation_j"] = round(float(rotation_j), 4)

    data_min = normalized.get("data_min")
    if data_min is not None:
        normalized["data_min"] = round(float(data_min), 3)

    data_max = normalized.get("data_max")
    if data_max is not None:
        normalized["data_max"] = round(float(data_max), 3)

    return normalized
