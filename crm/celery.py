import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")

# Use Redis as the broker
app.conf.broker_url = "redis://localhost:6379/0"

# Load task modules from all registered Django apps
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Optional: set timezone
app.conf.timezone = "Africa/Nairobi"

# Celery Beat schedule placeholder (loaded from settings.py)
