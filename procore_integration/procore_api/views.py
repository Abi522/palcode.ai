import logging
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from django.views.decorators.csrf import csrf_exempt

# Initialize logger
logger = logging.getLogger(__name__)


@api_view(['POST'])
@csrf_exempt
def procore_webhook(request):
    """
    API to process Procore webhook notifications for project creation, update, and deletion.
    """
    try:
        # ✅ Ensure request body is not empty
        if not request.body:
            logger.error("❌ Webhook received an empty body")
            return Response({"error": "Empty request body"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Validate JSON format
        try:
            data = json.loads(request.body.decode('utf-8'))  # Convert bytes to JSON
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON received: {str(e)}")
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

        event = data.get("event")
        project_id = str(data.get("resource_id"))  # Ensure project_id is a string
        project_name = data.get("name", "")

        logger.info(f"📩 Received Webhook: Event={event}, ProjectID={project_id}, Name={project_name}")

        # Validate request payload
        if not project_id:
            logger.error("❌ Missing 'resource_id'")
            return Response({"error": "Missing 'resource_id'"}, status=status.HTTP_400_BAD_REQUEST)

        if not event:
            logger.error("❌ Missing 'event'")
            return Response({"error": "Missing 'event'"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle project creation
        if event == "project.create":
            project, created = Project.objects.get_or_create(
                project_id=project_id,
                defaults={"name": project_name, "status": "created"}
            )

            if created:
                logger.info(f"✅ Project Created: {project_id} - {project_name}")
                return Response({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)

            if project_name and project.name != project_name:
                project.name = project_name
                project.status = "updated"
                project.save()
                logger.info(f"✅ Project Name Updated: {project.name}")
                return Response({"message": "Project name updated successfully"}, status=status.HTTP_200_OK)

            logger.info(f"ℹ️ Project Already Exists: {project_id}")
            return Response({"message": "Project already exists with no changes"}, status=status.HTTP_200_OK)

        # Handle project update
        elif event == "project.update":
            project = Project.objects.filter(project_id=project_id).first()
            if project:
                updated = False

                if project_name and project.name != project_name:
                    project.name = project_name
                    updated = True

                if project.status != "updated":
                    project.status = "updated"
                    updated = True

                if updated:
                    project.save()
                    logger.info(f"✅ Project Updated: {project_id}")
                    return Response({"message": "Project updated successfully"}, status=status.HTTP_200_OK)

                logger.info(f"ℹ️ No Changes for Project: {project_id}")
                return Response({"message": "No updates were made"}, status=status.HTTP_200_OK)

            logger.warning(f"⚠️ Update failed: Project not found - {project_id}")
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Handle project deletion
        elif event == "project.delete":
            project = Project.objects.filter(project_id=project_id).first()
            if project:
                project.delete()
                logger.info(f"❌ Project Deleted: {project_id}")
                return Response({"message": "Project deleted successfully"}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"⚠️ Delete failed: Project not found - {project_id}")
                return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            logger.warning(f"⚠️ Unknown event type received: {event}")
            return Response({"error": "Unsupported event type"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"🚨 Error processing webhook: {str(e)}", exc_info=True)
        return Response({"error": f"Webhook processing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""@csrf_exempt
def procore_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_type = data["event_type"]
        project_id = data["resource_id"]

        if event_type == "create" or event_type == "update":
            fetch_projects()  # Sync changes
        elif event_type == "delete":
            Project.objects.filter(procore_id=project_id).delete()

        return JsonResponse({"message": "Webhook received"}, status=200)"""





"""from django.http import JsonResponse
from  procore_api.utils import fetch_projects  # Import your function

def sync_procore_projects(request):
    fetch_projects()  # Call the function
    return JsonResponse({"message": "Projects synced successfully"})"""



































"""from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt  # Exempt from CSRF verification
@require_http_methods(["GET", "POST"])  # Accept both GET and POST requests
def webhook_receiver(request):
    if request.method == "GET":
        # Handle GET request (e.g., for testing purposes)
        return JsonResponse({"message": "Webhook receiver is active."}, status=200)
    elif request.method == "POST":
        try:
            payload = json.loads(request.body)
            # Process the payload here
            # For example, handle different event types:
            event_type = payload.get('event_type')
            if event_type == 'event_name':
                # Handle the specific event
                pass
            # Respond with a success status
            return HttpResponse(status=200)
        except json.JSONDecodeError:
            # Invalid JSON payload
            return HttpResponse(status=400)"""
