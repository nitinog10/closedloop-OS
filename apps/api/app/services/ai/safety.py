from fastapi import HTTPException


class SafetyService:
    blocked_terms = {'ignore all instructions', 'exfiltrate', 'dump secrets'}

    def validate_query(self, query: str) -> None:
        lowered = query.lower()
        if any(term in lowered for term in self.blocked_terms):
            raise HTTPException(status_code=400, detail='Query blocked by safety policy')
