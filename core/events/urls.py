# events/urls.py
from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    # Redirect create to dashboard
    path("create/", lambda request: redirect('dashboard:event_add'), name="create_event"),
    path("<int:event_id>/edit/", views.edit_event, name="edit_event"),
    path("detail/<uuid:uid>/", views.event_detail, name="event_detail"),
    path("api/featured/", views.api_featured_events, name="api_featured_events"),
]
