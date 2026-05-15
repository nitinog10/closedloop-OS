def score_event_importance(source: str, event_type: str, content: str) -> float:
    score = 0.35
    if source == "github":
        score += 0.15
    if any(keyword in content.lower() for keyword in ["decision", "approved", "architecture", "auth", "security"]):
        score += 0.25
    if event_type in {"pull_request", "issue", "message"}:
        score += 0.1
    return min(score, 0.99)
