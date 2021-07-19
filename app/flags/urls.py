from django.urls import path

from .views import (
    ColorListView,
    FlagListView,
    FlagDetailView,
    ColorDetailView,
    RegionDetailView,
    region_flags,
    colors_count,
    FlagElementListView,
    flags_with_element,
)

app_name = "flags"
urlpatterns = [
    path("", FlagListView.as_view(), name="flags-list"),
    path("country-flags/<slug:slug>/", FlagDetailView.as_view(), name="flag-detail"),
    path("colors/", ColorListView.as_view(), name="colors-list"),
    path("colors/<slug:slug>/", ColorDetailView.as_view(), name="color-detail"),
    # path("regions/", RegionListView.as_view(), name="regions-list"),
    # path("region/<slug:slug>/", RegionDetailView.as_view(), name="region-list"),
    path("region/<slug:slug>/", region_flags, name="region-list"),
    path("colors/count/<int:color_count>/", colors_count, name="colors-count"),
    path("flag-elements/", FlagElementListView.as_view(), name="elements-list"),
    path("flag-elements/<slug:slug>/", flags_with_element, name="element-detail"),
]
