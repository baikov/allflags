from app.flags.models import Region


def regions_menu(request):
    if request.user.is_superuser:
        regions = Region.objects.filter(parent=None).order_by("ordering")
    else:
        regions = Region.objects.filter(parent=None, is_published=True).order_by("ordering")

    return {"regions_menu": regions}
