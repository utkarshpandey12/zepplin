import hashlib
import json


def compute_content_hash(content: dict):
    content_str = json.dumps(content, sort_keys=True)
    hash_value = hashlib.sha256(content_str.encode()).hexdigest()
    return hash_value
