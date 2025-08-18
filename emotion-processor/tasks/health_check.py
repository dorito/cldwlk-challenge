from app.celery import app as celery_app

@celery_app.task
def health_check():
  return 1