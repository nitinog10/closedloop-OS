def build_memory_record(event: dict) -> dict:
    return {
        "summary": event.get("title") or event.get("event_type"),
        "source": event.get("source"),
        "content": event.get("content"),
    }
