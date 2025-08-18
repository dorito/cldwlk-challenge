from tasks import health_check as celery_health_check
from kafka import BrokerConnection
from app.logger import LOGGER
from app.config import Config
from app.database import init_db_session, SESSION
from sqlalchemy import text
from socket import AF_INET

class HealthCheckService:
    def check_kafka_health(self) -> bool:
      return self._check_celery_health() and self._check_kafka_health()

    def check_queue_health(self) -> bool:
      return self._check_celery_health() and self._check_database_health()

    def _check_celery_health(self) -> bool:
        try:
            result = celery_health_check.delay()
            result.get(timeout=10)
            return True
        except Exception as e:
            LOGGER.error(f"Celery health check failed: {e}")
            return False

    def _check_kafka_health(self) -> bool:
        try:
            kafka_host_data = Config.KAFKA_BOOTSTRAP_SERVERS.split(":")
            kafka_host = kafka_host_data[0]
            kafka_port = int(kafka_host_data[1])
            kafka_connection = BrokerConnection(kafka_host, kafka_port, AF_INET)
            kafka_connection.connect_blocking()
            if kafka_connection.connected():
                kafka_connection.close()
                return True
            raise Exception("connection error")
        except Exception as e:
            LOGGER.error(f"Kafka health check failed: {e}")
            return False
    
    def _check_database_health(self) -> bool:
        try:
            init_db_session()
            SESSION.execute(text('SELECT 1'))
            return True
        except Exception as e:
            LOGGER.error(f"Database health check failed: {e}")
            return False