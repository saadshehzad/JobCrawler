from django.urls import path
from .views import JobApplicationAutomationView

urlpatterns = [
    path('api/automate-job-applications/', JobApplicationAutomationView.as_view(), name='automate-job-applications'),
]
