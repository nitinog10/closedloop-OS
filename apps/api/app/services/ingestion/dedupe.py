import hashlib


def make_dedupe_key(source: str, source_event_id: str, content: str) -> str:
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    return f"{source}:{source_event_id}:{digest}"
