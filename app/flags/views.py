from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import (
    ColorGroup,
    MainFlag,
    Country,
    HistoricalFlag,
    BorderCountry,
    Color,
    Currency,
    Region,
    Subregion,
    FlagElement,
)


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


class FlagDetailView(DetailView):
    model = MainFlag
    template_name = "flags/flag-detail.html"
    context_object_name = "flag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        border_countries = []
        same_colors = []
        # Get all historical flags
        context["historical"] = HistoricalFlag.objects.filter(
            country__iso_code_a2=self.object.country.iso_code_a2
        ).order_by("from_year")

        # Get all border countries
        neighbours = BorderCountry.objects.filter(country=self.object.country)
        for row in neighbours:
            border_countries.append(row.border_country)
        context["neighbours"] = neighbours

        # Get all flag colors
        colors = Color.objects.filter(flags=self.object.id)
        context["colors"] = colors

        # Get flags with colors from same color groups
        if colors:
            for row in colors:
                same_colors.append(row.color_group)
            same_color_flags = MainFlag.objects.filter(colors__color_group=same_colors[0]).exclude(id=self.object.id)
            for i in range(1, len(colors)):
                same_color_flags = same_color_flags.filter(colors__color_group=same_colors[i])
            context["same_flags"] = same_color_flags

        # Get flags of border countries
        border_flags = MainFlag.objects.filter(country__in=border_countries)
        context["border_flags"] = border_flags

        # Set width and height for Download img block
        if self.object.proportion:
            height, width = self.object.proportion.split(":")
        else:
            height, width = 1, 2
        context["widths"] = {
            # 'w20': {'width': 20, 'height': int(20/int(width)*int(height))},
            "w40": {"width": 40, "height": int(40 / int(width) * int(height))},
            "w80": {"width": 80, "height": int(80 / int(width) * int(height))},
            "w160": {"width": 160, "height": int(160 / int(width) * int(height))},
            "w320": {"width": 320, "height": int(320 / int(width) * int(height))},
            "w640": {"width": 640, "height": int(640 / int(width) * int(height))},
            "w1280": {"width": 1280, "height": int(1280 / int(width) * int(height))},
            "w2560": {"width": 2560, "height": int(2560 / int(width) * int(height))},
        }
        context["heights"] = {
            "h20": {"width": int(20 / int(height) * int(width)), "height": 20},
            "h24": {"width": int(24 / int(height) * int(width)), "height": 24},
            "h40": {"width": int(40 / int(height) * int(width)), "height": 40},
            "h60": {"width": int(60 / int(height) * int(width)), "height": 60},
            "h80": {"width": int(80 / int(height) * int(width)), "height": 80},
            "h120": {"width": int(120 / int(height) * int(width)), "height": 120},
            "h240": {"width": int(240 / int(height) * int(width)), "height": 240},
        }
        context["country"] = Country.objects.get(id__exact=self.object.country.id)
        # context["currencies"] = Currency.objects.filter(countries=self.object.country.id)

        return context


class ColorListView(ListView):
    model = ColorGroup
    template_name = "flags/colors-list.html"
    context_object_name = "colors"


class ColorDetailView(DetailView):
    model = ColorGroup
    template_name = "flags/color-detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colors = Color.objects.filter(color_group=self.object.id)
        flags = MainFlag.objects.filter(colors__in=colors)

        context["flags"] = flags
        context["colors"] = colors
        return context


class RegionDetailView(DetailView):
    model = Subregion
    template_name = "flags/region-list.html"
    context_object_name = "region"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flags = MainFlag.objects.filter(country__subregion=self.object.id)

        context["flags"] = flags
        context["reg"] = self.object.region
        return context


def region_flags(request, slug):
    template_name = "flags/region-list.html"
    region = get_object_or_404(Subregion, slug=slug)
    countries = region.countries.all()
    flags = MainFlag.objects.filter(country__in=countries)

    context = {"region": region, "flags": flags}

    return render(request, template_name, context)


def colors_count(request, color_count):
    template_name = "flags/colors-count.html"
    flags = MainFlag.objects.annotate(num_colors=Count("colors")).filter(num_colors=color_count)
    context = {"flags": flags, "color_count": color_count}
    if flags:
        return render(request, template_name, context)
    else:
        raise Http404


class FlagElementListView(ListView):
    model = FlagElement
    template_name = "flags/elements-list.html"
    context_object_name = "elements"

    def get_queryset(self):
        elements = FlagElement.objects.annotate(flags_count=Count("flags_with_elem")).filter(flags_count__gt=0)
        return elements


def flags_with_element(request, slug):
    template_name = "flags/elements-list.html"
    flags = MainFlag.objects.filter(elements__slug=slug)
    element = FlagElement.objects.get(slug=slug)
    # We can take all elements or...
    # elements = FlagElement.objects.all()
    # we can take only not empty elements
    elements = FlagElement.objects.annotate(flags_count=Count("flags_with_elem")).filter(flags_count__gt=0)
    context = {"flags": flags, "element": element, "elements": elements}
    if flags:
        return render(request, template_name, context)
    else:
        raise Http404
