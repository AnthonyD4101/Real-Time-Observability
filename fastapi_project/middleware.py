from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        logger.info("Request: method=%s url=%s", request.method, request.url)
        response = await call_next(request)
        execution_time = time.time() - start_time
        logger.info("Response status: %d", response.status_code)
        logger.info("Execution time: %.2fs", execution_time)
        return response
