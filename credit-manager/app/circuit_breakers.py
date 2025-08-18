import pybreaker
from pydantic import ValidationError

celery_processing_breaker = pybreaker.CircuitBreaker(
    fail_max=1, reset_timeout=30, exclude=[ValidationError]
)
db_processing_breaker = pybreaker.CircuitBreaker(
    fail_max=5, reset_timeout=30, exclude=[ValidationError]
)
request_processing_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)
