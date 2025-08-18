from celery import Celery
from app.config import Config
from app.logger import LOGGER
from celery.signals import worker_init
from app.database import init_db_session

app = Celery('celery_app')
app.conf.update(
    broker_url=Config.CELERY_BROKER,
    result_backend=Config.CELERY_BACKEND,
    include=['tasks']
)

@worker_init.connect
def initialize_session(**kwargs):
    init_db_session()