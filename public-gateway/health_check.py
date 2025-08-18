import argparse

from app.config import Config
from app.logger import LOGGER, init_logging
from services import HealthCheckService

init_logging()

parser = argparse.ArgumentParser(
    prog=f"{Config.APP_NAME}-health-checker",
    description=f"Does the health check for {Config.APP_NAME}",
)
parser.add_argument(
    "--service",
    choices=["queue", "api"],
    help="Which services can be health checked",
    required=True,
)
args = parser.parse_args()
service = HealthCheckService()
result = False
match args.service:
    case "queue":
        result = service.check_queue_health()
    case "api":
        result = service.check_api_health()
    case _:
        raise Exception(f"Unknown worker type: {args.worker}")

if result is not False:
    exit(0)
exit(1)
