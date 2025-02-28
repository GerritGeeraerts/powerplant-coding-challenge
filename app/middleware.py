import logging
import time
from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses
    """
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        
        # Log the request
        logger.info(
            f"Request {request_id} started: {request.method} {request.url.path}"
        )
        
        # Log request headers in debug level
        headers = dict(request.headers.items())
        # Remove sensitive information
        if 'authorization' in headers:
            headers['authorization'] = "***"
        logger.debug(f"Request {request_id} headers: {headers}")
        
        # Process the request and measure time
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Log the response
            process_time = time.time() - start_time
            logger.info(
                f"Request {request_id} completed: {request.method} {request.url.path} "
                f"- Status: {response.status_code} - Duration: {process_time:.3f}s"
            )
            
            return response
            
        except Exception as e:
            # Log any exceptions that occur during request handling
            process_time = time.time() - start_time
            logger.error(
                f"Request {request_id} failed: {request.method} {request.url.path} "
                f"- Duration: {process_time:.3f}s - Error: {str(e)}"
            )
            raise