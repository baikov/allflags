# from django.db.models import Count
# from django.http import Http404
# from django.shortcuts import render
from django.views.generic import ListView

from .models import MainFlag


class FlagListView(ListView):
    model = MainFlag
    template_name = "flags/flags-list.html"
    context_object_name = "flags"
    # paginate_by = 20

    def get_queryset(self):
        flags = MainFlag.objects.all()
        if not self.request.user.is_superuser:
            flags = flags.published()
        return flags.order_by("country__name")
