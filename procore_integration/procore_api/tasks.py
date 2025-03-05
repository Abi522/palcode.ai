from celery import shared_task
from procore_api.utils import fetch_projects

@shared_task
def sync_procore_projects_task():
    fetch_projects()
