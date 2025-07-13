from .celery import app as celery_app
import django_crontab

__all__ = ('celery_app',)
