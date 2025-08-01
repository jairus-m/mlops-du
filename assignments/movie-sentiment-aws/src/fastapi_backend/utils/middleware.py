"""
FastAPI-specific middleware utilities.
"""
import logging
from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def log_middleware_request(request: Request, call_next) -> Response:
    """Middleware to log incoming requests."""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response


async def log_middleware_response(request: Request, call_next) -> Response:
    """Middleware to log outgoing responses."""
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
