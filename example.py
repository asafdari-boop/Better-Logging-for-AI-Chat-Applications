from fastapi import FastAPI
from starlette.applications import Starlette
import logging
from middleware import middleware
from logger import setup_logging
import uvicorn

# Set up logging first
setup_logging()

# Create logger for this module
logger = logging.getLogger(__name__)

# Create FastAPI app with our custom middleware
app = FastAPI(middleware=middleware)

@app.get("/chat/{chat_id}")
async def chat_endpoint(chat_id: str):
    """
    Example endpoint that uses the chat_id from the URL path.
    The chat_id will automatically be added to logs via the middleware.
    """
    logger.info("Received request")
    return {"message": f"Processing chat {chat_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
