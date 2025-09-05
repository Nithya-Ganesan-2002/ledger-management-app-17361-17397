from .app import app

# PUBLIC_INTERFACE
def get_app():
    """Return the FastAPI application instance for ASGI servers."""
    return app
