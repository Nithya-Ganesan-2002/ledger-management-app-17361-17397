from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health Check", operation_id="health_check", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON message indicating service is healthy.
    """
    return {"message": "Healthy"}
