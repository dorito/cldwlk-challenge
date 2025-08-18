from socket import AF_INET

from kafka import BrokerConnection

from sqlalchemy import text

from app.config import Config
from app.database import DbSession, init_db_session
from app.logger import LOGGER


class HealthCheckService:
    def check_api_health(self) -> bool:
        return self._check_database_health() and self._check_kafka_health()

    def _check_database_health(self) -> bool:
        try:
            init_db_session()
            DbSession.execute(text("SELECT 1"))
            return True
        except Exception as e:
            LOGGER.error(f"Database health check failed: {e}")
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
