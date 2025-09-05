import uvicorn
from .services.bootstrap import bootstrap_sync

if __name__ == "__main__":
    # Initialize database schema and seed minimal data
    bootstrap_sync()
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=False)
