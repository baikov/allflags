from django.urls import path

from .views import (
    ColorListView,
    FlagListView,
    FlagDetailView,
    ColorDetailView,
    RegionListView,
    colors_count,
    FlagElementListView,
    flags_with_element,
    flags_by_region,
    # flag_detail,
)

app_name = "flags"
urlpatterns = [
    path("", FlagListView.as_view(), name="flags-list"),
    path("<slug:slug>/", FlagDetailView.as_view(), name="flag-detail"),
    # By regions
    path("regions/", RegionListView.as_view(), name="regions-list"),
    path("regions/<slug:region_slug>/", flags_by_region, name="region-flags"),
    path("regions/<slug:region_slug>/<slug:subregion_slug>/", flags_by_region, name="subregion-flags"),
    # By colors
    path("colors/", ColorListView.as_view(), name="colors-list"),
    path("colors/<slug:slug>/", ColorDetailView.as_view(), name="color-detail"),
    path("colors/count/<int:color_count>/", colors_count, name="colors-count"),
    # By elements
    path("flag-elements/", FlagElementListView.as_view(), name="elements-list"),
    path("flag-elements/<slug:slug>/", flags_with_element, name="element-detail"),
    # By countries
    # path("countries/", countries_list, name="countries-list"),
    # path("countries/<slug:slug>/", country_detail, name="country-detail"),
    # path("countries/<slug:country_slug>/<slug:flag_slug>/", flag_detail, name="flag-detail"),
]
