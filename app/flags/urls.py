from django.urls import path

from .views import FlagListView

app_name = "flags"
urlpatterns = [
    path("", FlagListView.as_view(), name="flags-list"),
]
