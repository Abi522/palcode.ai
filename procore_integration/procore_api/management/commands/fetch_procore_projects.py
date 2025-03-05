import requests
from django.core.management.base import BaseCommand
from procore_api.models import Project

class Command(BaseCommand):
    help = "Fetch projects from Procore and update the database"

    def handle(self, *args, **kwargs):
        access_token = "your_access_token_here"  # Fetch dynamically if needed
        headers = {"Authorization": f"Bearer {access_token}"}

        url = "https://api.procore.com/vapid/projects"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            for project in response.json():
               Project.objects.update_or_create(
                    procore_id=project["id"],
                    defaults={
                        "name": project["name"],
                        "status": project["status"],
                        "created_at": project["created_at"],
                        "updated_at": project["updated_at"]
                    }
                )
            self.stdout.write(self.style.SUCCESS("Successfully updated Procore projects"))
        else:
            self.stderr.write(self.style.ERROR("Failed to fetch Procore projects"))
