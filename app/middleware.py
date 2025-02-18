from fastapi import Request
from fastapi.responses import JSONResponse
from .logger import setup_logger

logger = setup_logger(__name__)

async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(e)}
        ) 