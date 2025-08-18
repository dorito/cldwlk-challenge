import pybreaker
from pydantic import ValidationError

kafka_processing_breaker = pybreaker.CircuitBreaker(
    fail_max=1, reset_timeout=30, exclude=[ValidationError]
)
db_processing_breaker = pybreaker.CircuitBreaker(
    fail_max=5, reset_timeout=30, exclude=[ValidationError]
)
