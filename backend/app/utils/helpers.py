import json
import uuid
import time
import random
from functools import wraps


# =========================
# SAFE DICT ACCESS
# =========================
def safe_get(data: dict, key: str, default=None):
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


# =========================
# JSON PARSER (SAFE)
# =========================
def safe_json_loads(text: str):
    try:
        return json.loads(text)
    except Exception:
        return {}


# =========================
# GENERATE UNIQUE ID
# =========================
def generate_id(prefix: str = ""):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


# =========================
# RETRY DECORATOR
# =========================
def retry(times: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            last_error = None

            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    time.sleep(delay)

            raise last_error

        return wrapper
    return decorator


# =========================
# RANDOM SELECTOR
# =========================
def weighted_choice(items: list, weights: list):
    return random.choices(items, weights=weights, k=1)[0]


# =========================
# CLEAN EMPTY VALUES
# =========================
def clean_dict(data: dict):
    return {
        k: v for k, v in data.items()
        if v is not None and v != ""
    }