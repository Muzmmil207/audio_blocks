from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("", views.get_routes),
    path("audio-api/", views.AudioListView.as_view(), name="audio-api"),
    path("audio-api/<str:id>/", views.AudioElementDetailsView.as_view(), name="audio-details-api"),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])
