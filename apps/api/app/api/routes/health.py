from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the API is running and healthy. Returns a simple status message.",
    response_description="Health status of the API",
    responses={
        200: {
            "description": "API is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "healthy"}
                }
            }
        }
    }
)
async def health() -> dict[str, str]:
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        dict: Status message indicating the API is healthy
    """
    return {"status": "healthy"}
