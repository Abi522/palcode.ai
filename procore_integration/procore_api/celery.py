from celery.schedules import crontab

from procore_api.webhook_receiver import app

app.conf.beat_schedule = {
    "sync-procore-projects-every-hour": {
        "task": "your_app.tasks.sync_procore_projects_task",
        "schedule": crontab(minute=0, hour="*"),
    },
}
