from datetime import date, datetime

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from .models import BorderCountry, HistoricalFlag, MainFlag

# from config.settings.base import MEDIA_ROOT


# ORM queries for flag detail
def get_flag_or_404(request, flag_slug: str) -> MainFlag:
    if request.user.is_superuser:
        flag = get_object_or_404(
            MainFlag.objects.select_related("country", "country__region").prefetch_related("elements", "facts"),
            slug=flag_slug,
        )
    else:
        flag = get_object_or_404(
            MainFlag.objects.select_related("country", "country__region").prefetch_related("elements", "facts"),
            slug=flag_slug,
            is_index=True,
            is_published=True,
        )

    return flag


def get_emoji(iso2: str) -> str:
    OFFSET = ord("🇦") - ord("A")
    return chr(ord(iso2[0]) + OFFSET) + chr(ord(iso2[1]) + OFFSET)


def get_historical_flags(iso2: str) -> QuerySet:

    return HistoricalFlag.objects.prefetch_related("pictures").filter(country__iso_code_a2=iso2)


def get_neighbours(country_id: int) -> QuerySet:
    return (
        BorderCountry.objects
        .select_related("border_country")
        .filter(country__id=country_id)
        # .prefetch_related("")
    )


def get_neighbours_flags(neighbours_id: list[int]) -> QuerySet:
    return (
        MainFlag.objects.select_related("country")
        .filter(country__id__in=neighbours_id)
    )


def get_flags_with_same_colors(flag_id: int, same_color_groups: list) -> QuerySet:
    return (
        MainFlag.objects.select_related("country")
        .filter(colors_set__color_group__slug__in=same_color_groups)
        .exclude(id=flag_id).distinct()
    )


def get_flag_age(adopted_date: date) -> int:
    if adopted_date:
        return int(datetime.now().strftime("%Y")) - int(adopted_date.strftime("%Y"))
    else:
        return 0
