from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from import_export import resources

# from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats
import tablib

from .models import (
    BorderCountry,
    Color,
    ColorGroup,
    Country,
    Currency,
    FlagElement,
    # Region,
    # Subregion,
    MainFlag,
    FlagEmoji,
    HistoricalFlag,
    FlagFact,
    Region
)


class SCSV(base_formats.CSV):
    def get_title(self):
        return "scsv"

    def create_dataset(self, in_stream, **kwargs):
        kwargs["delimiter"] = ";"
        kwargs["format"] = "csv"
        return tablib.import_set(in_stream, **kwargs)
        # return super().create_dataset(in_stream, **kwargs)


class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency


class CurrencyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("ru_name", "iso_code")
    search_fields = ["ru_name", "iso_code"]
    filter_horizontal = ("countries",)
    resource_class = CurrencyResource

    def get_import_formats(self):
        # self.formats += [SCSV]
        # return [f for f in self.formats if f().can_import()]
        return self.formats + [
            SCSV,
        ]


class BorderCountryInline(admin.TabularInline):
    model = BorderCountry
    extra = 2
    fk_name = "country"
    raw_id_fields = ("border_country",)


class CurrencyInline(admin.TabularInline):
    model = Currency.countries.through
    extra = 1


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("iso_code_a2",)}
    list_display = (
        "name",
        "iso_code_a2",
        "slug",
        "is_published",
    )
    list_filter = ["region"]
    search_fields = ["name", "iso_code_a2"]
    readonly_fields = ["updated_date", "created_date"]
    inlines = (BorderCountryInline, CurrencyInline)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "region",
                    "name",
                    "iso_code_a2",
                    "slug",
                    "conventional_long_name",
                    "local_long_name",
                    "local_short_name",
                    "anthem",
                    "motto",
                    "official_language",
                    "phone_code",
                    "internet_tld",
                ]
            },
        ),
        (
            _("Name cases"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    ("ru_name_rod", "ru_name_dat", "ru_name_vin", "ru_name_tvo", "ru_name_pre"),
                ],
            },
        ),
        (
            _("ISO"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    ("iso_code_a3", "iso_code_num"),
                ],
            },
        ),
        (
            _("Government"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "en_short_form",
                    "en_long_form",
                    "ru_capital_name",
                    "en_capital_name",
                    "ru_government_type",
                    "ru_chief_of_state",
                    "ru_head_of_government",
                    "en_government_type",
                    "en_chief_of_state",
                    "en_head_of_government",
                ],
            },
        ),
        (
            _("Area and population"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    ("area_total", "area_land", "area_water", "coastline", "area_global_rank"),
                    ("population_total", "population_date", "population_global_rank"),
                ],
            },
        ),
        (
            _("Economic"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    ("gdp_value", "gdp_date", "gdp_global_rank"),
                    ("external_debt_value", "external_debt_date", "external_debt_global_rank"),
                    "info_updated",
                ],
            },
        ),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "seo_title",
                    "seo_description",
                    "seo_h1",
                    "is_published",
                    "is_index",
                    "is_follow",
                    "created_date",
                    "updated_date",
                ],
            },
        ),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CountryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["seo_description"].widget.attrs["rows"] = 2
        form.base_fields["seo_description"].widget.attrs["cols"] = 10  # doesn't work...
        return form

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }


class ColorGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ["name"]
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "slug", "short_name", "description", "colorgroup_meanings"],
            },
        ),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": ["seo_title", "seo_description", "seo_h1", "is_published", "is_index", "is_follow"],
            },
        ),
    ]


class ColorAdmin(admin.ModelAdmin):
    # list_display = ('color_group', 'hex', 'rgb', 'cmyk', 'get_flags')
    list_display = ("color_group", "color_html", "hex", "rgb", "cmyk")
    search_fields = ["color_group", "hex", "rgb"]
    # list_filter = ['color_group']
    # inlines = [FlagInline]

    # def get_flags(self, obj):
    #     return obj.flags.first()
    # return obj.flags.all().values('title')

    def color_html(self, obj):
        return format_html(f'<div style="background-color:#{obj.hex};width:90%;height:1rem;"></div>')


class FlagElementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ["name"]
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "slug", "description"],
            },
        ),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": ["seo_title", "seo_description", "seo_h1", "is_published", "is_index", "is_follow"],
            },
        ),
    ]


class FlagEmojiInline(admin.TabularInline):
    model = FlagEmoji
    extra = 1
    fields = ("unicode", "slug")


class FlagFactInline(admin.TabularInline):
    model = FlagFact
    extra = 1
    fields = ("caption", "text")


class FlagEmojiAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("name",)}
    list_display = ("unicode", "flag")
    search_fields = ["flag"]
    fieldsets = [
        (
            None,
            {
                "fields": ["flag", "slug", "unicode", "description"],
            },
        ),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": ["seo_title", "seo_description", "seo_h1", "is_published", "is_index", "is_follow"],
            },
        ),
    ]


class MainFlagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("country", "title", "slug", "is_published")
    search_fields = ["title", "country__name"]
    list_filter = ["colors__color_group"]
    raw_id_fields = ("country",)
    readonly_fields = ["updated_date", "created_date"]
    filter_horizontal = ("colors", "elements")
    inlines = (FlagEmojiInline, FlagFactInline)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "country",
                    "title",
                    "slug",
                    "name",
                    "adopted_date",
                    "flag_day",
                    "proportion",
                    "colors",
                    "short_description",
                    "construction_image",
                    "design_description",
                    "history_text",
                ]
            },
        ),
        (
            _("Elements"),
            {
                "classes": ("collapse", "wide", "extrapretty"),
                "fields": [
                    "elements",
                ],
            },
        ),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "seo_title",
                    "seo_description",
                    "seo_h1",
                    "is_published",
                    "is_index",
                    "is_follow",
                    "dl_imgs",
                ],
            },
        ),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(MainFlagAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["seo_description"].widget.attrs["rows"] = 2
        form.base_fields["seo_description"].widget.attrs["cols"] = 10  # doesn't work...
        return form

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }


class HistoricalFlagAdmin(admin.ModelAdmin):
    list_display = ("from_year", "to_year", "country", "title")
    search_fields = ["title", "from_year", "country__name"]
    list_filter = ["country__name"]
    raw_id_fields = ("country",)
    fieldsets = [
        (None, {"fields": ["country", "title", "image_url", "svg_file", ("from_year", "to_year"), "description"]}),
    ]


class FlagFactAdmin(admin.ModelAdmin):
    list_display = ("flag", "caption", "label")
    search_fields = ["flag__name", "caption", "label"]
    list_filter = ["flag__name"]
    raw_id_fields = ("flag",)
    fieldsets = [
        (None, {"fields": ["flag", "caption", "label", "text", "image"]}),
    ]


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("ordering", "is_published",)
    list_display = ("name", "slug", "parent", "ordering", "is_published",)
    list_filter = ["parent"]
    search_fields = ["name", "parent__name"]
    fieldsets = [
        (None, {"fields": ["parent", "name", "slug", "ordering", "description"]}),
        (
            _("SEO"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "seo_title",
                    "seo_description",
                    "seo_h1",
                    "is_published",
                    "is_index",
                    "is_follow",
                ],
            },
        ),
    ]


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ColorGroup, ColorGroupAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(FlagElement, FlagElementAdmin)
admin.site.register(MainFlag, MainFlagAdmin)
admin.site.register(FlagEmoji, FlagEmojiAdmin)
admin.site.register(HistoricalFlag, HistoricalFlagAdmin)
admin.site.register(FlagFact, FlagFactAdmin)

# admin.site.register(Region, RegionAdmin)
# admin.site.register(Subregion, SubregionAdmin)


# class RegionAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ("name", "slug")
#     search_fields = ["name"]
#     fieldsets = [
#         (None, {"fields": ["name", "slug", "description"]}),
#         (
#             _("SEO"),
#             {
#                 "classes": ("collapse", "wide"),
#                 "fields": [
#                     "seo_title",
#                     "seo_description",
#                     "seo_h1",
#                     "is_published",
#                     "is_index",
#                     "is_follow",
#                 ],
#             },
#         ),
#     ]


# class SubregionAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ("name", "slug", "region")
#     search_fields = ["name", "region"]
#     fieldsets = [
#         (None, {"fields": ["region", "name", "slug", "description"]}),
#         (
#             _("SEO"),
#             {
#                 "classes": ("collapse", "wide"),
#                 "fields": [
#                     "seo_title",
#                     "seo_description",
#                     "seo_h1",
#                     "is_published",
#                     "is_index",
#                     "is_follow",
#                 ],
#             },
#         ),
#     ]
