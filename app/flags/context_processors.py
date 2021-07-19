from app.flags.models import Region


def regions_menu(request):
    # categories = Region.objects.filter(parent=None)
    regions = Region.objects.all()

    return {"regions_menu": regions}
