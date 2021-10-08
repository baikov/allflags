import logging
from datetime import datetime
from django.views.decorators.http import last_modified  # condition
# from django.http import HttpResponse

from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
# from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import (  # Region,; Subregion,; Currency,
    BorderCountry,
    Color,
    ColorGroup,
    Country,
    FlagElement,
    HistoricalFlag,
    MainFlag,
    Region,
)
from .services import (  # get_files
    get_emoji,
    get_flag_age,
    get_flag_or_404,
    get_flags_with_same_colors,
    get_historical_flags,
    get_neighbours,
    get_neighbours_flags,
)

logger = logging.getLogger(__name__)


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

        if self.request.user.is_superuser:
            flag = get_object_or_404(MainFlag, slug=self.object.slug)
        else:
            flag = get_object_or_404(MainFlag, slug=self.object.slug, is_index=True, is_published=True)

        context["flag"] = flag
        border_countries = []
        same_colors = []
        # Get all historical flags
        context["historical"] = HistoricalFlag.objects.filter(
            country__iso_code_a2=self.object.country.iso_code_a2
        ).order_by("ordering")

        # Get all border countries
        neighbours = BorderCountry.objects.filter(country=self.object.country)
        for row in neighbours:
            border_countries.append(row.border_country)
        context["neighbours"] = neighbours

        # Get all flag colors
        # colors = Color.objects.filter(flags=self.object.id)
        colors = Color.objects.filter(flag=self.object.id, is_main=True).order_by("ordering")
        context["colors"] = colors
        context["comp_colors"] = Color.objects.filter(flag=self.object.id, is_main=False)

        # Get colors adjective
        adj = ""
        if len(colors) > 1:
            for i in range(len(colors) - 1):
                adj += str(colors[i].color_group.short_name).lower()
                adj += "-"
            adj += str(colors[len(colors) - 1].color_group.name).lower()
        context["colors_adj"] = adj

        # Get flags with colors from same color groups
        if colors:
            for row in colors:
                same_colors.append(row.color_group)
            same_color_flags = MainFlag.objects.filter(colors_set__color_group=same_colors[0]).exclude(
                id=self.object.id
            )
            for i in range(1, len(colors)):
                same_color_flags = same_color_flags.filter(colors_set__color_group=same_colors[i])
            context["same_flags"] = same_color_flags

        # Get flags of border countries
        border_flags = MainFlag.objects.filter(country__in=border_countries)
        context["border_flags"] = border_flags
        context["border_flags_h2"] = f"Флаги соседних с {flag.country.ru_name_tvo} стран"

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
        if flag.adopted_date:
            context["age"] = int(datetime.now().strftime("%Y")) - int(flag.adopted_date.strftime("%Y"))

        return context


class ColorListView(ListView):
    model = ColorGroup
    template_name = "flags/colors-list.html"
    context_object_name = "colors"
    # ordering = ['colors']

    def get_queryset(self):
        qs = ColorGroup.objects.published().annotate(num_colors=Count("colors")).order_by("-num_colors")
        return qs

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "-date_created")
        # validate ordering here
        return ordering

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        last_group = self.get_queryset().latest("updated_date")
        response["Last-Modified"] = last_group.updated_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    # def head(self, *args, **kwargs):
    #     last_group = self.get_queryset().latest("updated_date")
    #     response = HttpResponse(
    #         # RFC 1123 date format.
    #         headers={'Last-Modified': last_group.updated_date},  # .strftime('%a, %d %b %Y %H:%M:%S GMT')
    #     )
    #     return response


class ColorDetailView(DetailView):
    model = ColorGroup
    template_name = "flags/color-detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colors = Color.objects.filter(color_group=self.object.id)
        flags = MainFlag.objects.filter(colors_set__in=colors)

        context["flags"] = flags
        context["colors"] = colors
        return context


class RegionListView(ListView):
    model = Region
    template_name = "flags/region-list.html"
    context_object_name = "regions"

    def get_queryset(self):
        regions = Region.objects.filter(parent=None)
        if not self.request.user.is_superuser:
            regions = regions.published()
        return regions.order_by("ordering")


def flags_by_region(request, region_slug, subregion_slug=None):
    template_name = "flags/flags-by-region.html"
    if subregion_slug:
        region = get_object_or_404(Region, slug=subregion_slug)
        if not region.is_published and not request.user.is_superuser:
            raise Http404
        else:
            countries = region.countries.all()
    else:
        region = get_object_or_404(Region, slug=region_slug, parent=None)
        if not region.is_published and not request.user.is_superuser:
            raise Http404
        else:
            subregions = region.subregions.filter(is_published=True)
            countries = Country.objects.filter(region__in=subregions).order_by("ordering")

    flags = MainFlag.objects.filter(country__in=countries)

    context = {"region": region, "flags": flags}

    return render(request, template_name, context)


def colors_count(request, color_count):
    template_name = "flags/colors-count.html"
    # flags = MainFlag.objects.annotate(num_colors=Count("colors_set")).filter(num_colors=color_count)
    main_colors = Color.objects.filter(is_main=True)
    flags = MainFlag.objects.filter(colors_set__in=main_colors)
    flags = flags.annotate(num_colors=Count("colors_set")).filter(num_colors=color_count)
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


def flag_last_modified(reqest, flag_slug):
    last_mod = MainFlag.objects.get(slug=flag_slug).updated_date
    # last_mod = datetime.combine(flag.updated_date, datetime.min.time())
    return last_mod


# @condition(last_modified_func=flag_last_modified)
@last_modified(flag_last_modified)
def flag_detail(request, flag_slug):
    template_name = "flags/flag-detail.html"

    flag = get_flag_or_404(request, flag_slug)
    neighbours = get_neighbours(flag.country.id)
    border_flags = get_neighbours_flags(neighbours.values("border_country__id"))
    main_colors = flag.colors_set.select_related("color_group").filter(is_main=True)
    # complementary_colors = flag.colors_set.select_related("color_group").filter(is_main=False)
    historical = get_historical_flags(flag.country.iso_code_a2)
    same_color_groups = flag.colors_set.filter(is_main=True).values("color_group__slug")
    # logger.info(same_color_groups)
    same_color_flags = get_flags_with_same_colors(flag.id, same_color_groups)
    emoji = get_emoji(flag.country.iso_code_a2)
    age = get_flag_age(flag.adopted_date)
    # files = get_files(flag.id)
    files = flag.downloads.filter(is_show_on_detail=True)
    files_count = len(flag.downloads.all())
    main_picture = files.filter(is_main=True).first()
    # adj = ""
    # if len(colors) > 1:
    #     for i in range(len(colors) - 1):
    #         adj += str(colors[i].color_group.short_name).lower()
    #         adj += "-"
    #     adj += str(colors[len(colors) - 1].color_group.name).lower()

    context = {
        "flag": flag,
        "historical": historical,
        "neighbours": neighbours,
        "colors": main_colors,
        # "complementary_colors": complementary_colors,
        "same_flags": same_color_flags,
        "border_flags": border_flags,
        "emoji": emoji,
        # "widths": widths,
        # "heights": heights,
        "age": age,
        "files": files,
        "files_count": files_count,
        "main_picture": main_picture,
        # "colors_adj": adj,
    }

    return render(request, template_name, context)


# def region_list(request):
#     template_name = "flags/region-list.html"
#     regions = get_object_or_404(Subregion, slug=slug)
#     countries = region.countries.all()
#     flags = MainFlag.objects.filter(country__in=countries)

#     context = {"region": region, "flags": flags}

#     return render(request, template_name, context)
