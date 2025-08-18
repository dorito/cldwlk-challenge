import argparse

from app.logger import LOGGER, init_logging
from services.health_check import HealthCheckService

init_logging()

parser = argparse.ArgumentParser(
    prog="emotion-processor-health-checker",
    description="Does the health check for emotion-processor",
)
parser.add_argument(
    "--service",
    choices=["kafka", "queue"],
    help="Which services can be health checked",
    required=True,
)
args = parser.parse_args()
service = HealthCheckService()
result = False
match args.service:
    case "kafka":
        result = service.check_kafka_health()
    case "queue":
        result = service.check_queue_health()
    case _:
        raise Exception(f"Unknown worker type: {args.worker}")

if result is not False:
    exit(0)
exit(1)
