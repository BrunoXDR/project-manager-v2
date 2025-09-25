# src/project_management_api/infrastructure/api/middleware.py
import time
import json
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        log_dict = {
            "url": str(request.url),
            "method": request.method,
            "status_code": response.status_code,
            "process_time_ms": round(process_time)
        }

        logger.info(json.dumps(log_dict))
        return response