from django.urls import path
from .views import procore_webhook
from django.urls import path
#from .views import webhook_receiver
#from .views import sync_procore_projects


urlpatterns = [
    path('procore/webhook/', procore_webhook, name='procore_webhook'),
   # path('webhook/', webhook_receiver, name='webhook_receiver'),
    #path("sync-projects/", sync_procore_projects, name="sync_procore_projects"),
]
