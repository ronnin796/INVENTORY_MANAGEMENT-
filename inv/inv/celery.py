from celery import Celery
from celery.schedules import crontab
import os



# Tell Celery where Django settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inv.settings")



app = Celery("inv",
             broker="redis://127.0.0.1:6379/0",
             backend="redis://127.0.0.1:6379/0")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Schedule forecasts daily at 2 AM
app.conf.beat_schedule = {
    "update-forecasts-daily": {
        "task": "forecast.tasks.update_forecasts_for_all_products",
        "schedule": crontab(hour=2, minute=0),
    },
}
