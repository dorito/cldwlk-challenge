import argparse

from app.config import Config
from app.logger import LOGGER, init_logging
from services import KafkaWorkerService

init_logging()

parser = argparse.ArgumentParser(
    prog=f"{Config.APP_NAME}-worker",
    description=f"Does the {Config.APP_NAME} processing for ECS",
)
parser.add_argument(
    "--worker", choices=["kafka"], help="Which workers to initiate", required=True
)
args = parser.parse_args()

match args.worker:
    case "kafka":
        LOGGER.info("Starting Kafka worker...")
        worker = KafkaWorkerService()
        worker.handle()
    case _:
        raise Exception(f"Unknown worker type: {args.worker}")
