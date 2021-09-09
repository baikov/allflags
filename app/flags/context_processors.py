from django.db.models import Count

from app.flags.models import Region


def regions_menu(request):
    if request.user.is_superuser:
        regions = Region.objects.prefetch_related("subregions").filter(parent=None).order_by("ordering")
        subregions = Region.objects.select_related("parent").annotate(countries_count=Count("countries"))
    else:
        # regions = (
        #     Region.objects.prefetch_related("subregions").filter(parent=None, is_published=True).order_by("ordering")
        # )
        regions = (
            Region.objects.prefetch_related("subregions").filter(parent=None, is_published=True).order_by("ordering")
        )
        subregions = (
            Region.objects.select_related("parent")
            .filter(is_published=True)
            .annotate(countries_count=Count("countries"))
        )

    return {"regions_menu": regions, "subregions": subregions}
