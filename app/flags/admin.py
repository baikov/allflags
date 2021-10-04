import tablib
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from imagekit.admin import AdminThumbnail
from import_export import resources
# from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from .models import (  # Region, Subregion,; HistoricalFlagImage,
    BorderCountry,
    Color,
    ColorGroup,
    Country,
    Currency,
    FlagElement,
    FlagEmoji,
    FlagFact,
    HistoricalFlag,
    MainFlag,
    Picture,
    Region,
)


class ParentRegionListFilter(admin.SimpleListFilter):
    title = _("Main region")

    parameter_name = "main-region"

    def lookups(self, request, model_admin):
        return (
            ("main", _("Parent")),
            ("asia", _("Asia")),
            ("europe", _("Europe")),
            ("america", _("America")),
            ("africa", _("Africa")),
            ("oceaniya", _("Okeaniya")),
        )

    def queryset(self, request, queryset):
        if self.value() == "main":
            return queryset.filter(parent=None)
        if self.value() == "asia":
            return queryset.filter(parent__name="Азия")
        if self.value() == "europe":
            return queryset.filter(parent__name="Европа")
        if self.value() == "america":
            return queryset.filter(parent__name="Америка")
        if self.value() == "africa":
            return queryset.filter(parent__name="Африка")
        if self.value() == "oceaniya":
            return queryset.filter(parent__name="Океания")


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


class BorderCountryAdmin(admin.ModelAdmin):
    list_display = ("country", "border_country", "border")
    search_fields = [
        "country",
    ]
    list_editable = ("border",)
    raw_id_fields = ("country", "border_country",)


class BorderCountryInline(admin.TabularInline):
    model = BorderCountry
    extra = 2
    fk_name = "country"
    raw_id_fields = ("border_country",)


class CurrencyInline(admin.TabularInline):
    model = Currency.countries.through
    raw_id_fields = ("currency",)
    extra = 1


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("iso_code_a2",)}
    list_display = (
        "name",
        "iso_code_a2",
        "slug",
        "is_published",
    )
    list_editable = ("is_published",)
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
                    # "map_iframe",
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

    # formfield_overrides = {
    #     models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    # }


class ColorGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "ordering", "is_published")
    search_fields = ["name"]
    list_editable = ("ordering", "is_published",)
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "slug", "ordering", "short_name", "description", "colorgroup_meanings"],
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
    list_display = ("color_group", "flag", "color_html", "hex", "rgb", "cmyk", "ordering")
    list_editable = ("ordering",)
    search_fields = ["color_group__name", "hex", "rgb", "flag__country__name"]
    raw_id_fields = ("flag",)
    # list_filter = ['flag']

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "color_group",
                    "flag",
                    ("is_main", "ordering"),
                    "meaning",
                    "hex",
                    "rgb",
                    "cmyk",
                    "hsl",
                    "pantone"
                ],
            },
        )
    ]

    def color_html(self, obj):
        return format_html(f'<div style="background-color:#{obj.hex};width:90%;height:1rem;"></div>')


class FlagElementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "is_published")
    list_editable = ("is_published",)
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


class ColorInline(admin.TabularInline):
    model = Color
    extra = 1
    fields = ("is_main", "color_group", "ordering", "hex", "rgb", "pantone")


class FlagFactInline(admin.TabularInline):
    model = FlagFact
    extra = 1
    fields = ("ordering", "caption", "text", "is_published")


class DownloadablePictureFileInline(admin.TabularInline):
    model = DownloadablePictureFile
    extra = 1


@admin.register(DownloadablePictureFilePreview)
class DownloadablePictureFilePreviewAdmin(admin.ModelAdmin):
    list_display = ("flag", "thumbnail")
    readonly_fields = ['thumb']
    search_fields = ["flag"]
    # list_filter = ["content_type"]
    thumbnail = AdminThumbnail(image_field='thumb')
    inlines = (DownloadablePictureFileInline,)
    raw_id_fields = ("flag",)


class DownloadablePictureFilePreviewInline(admin.TabularInline):
    model = DownloadablePictureFilePreview
    extra = 1
    fields = ("is_main", "is_show_on_detail", "ordering", "image", "is_published")

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
    readonly_fields = [
        "updated_date", "created_date", "construction_webp", "construction_image_small", "construction_webp_small"
    ]
    filter_horizontal = ("colors", "elements")
    inlines = (ColorInline, FlagEmojiInline, FlagFactInline)
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
                    "proportion",
                    "short_description",
                    ("construction_url", "construction_image"),
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
        (
            _("Pictures"),
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "construction_webp", "construction_image_small", "construction_webp_small"
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


class PictureAdmin(admin.ModelAdmin):
    list_display = ("id", "thumbnail", "alt", "image", "ordering")
    readonly_fields = ["webp", "image_md", "webp_md", "image_xs", "webp_xs", "thumb"]
    search_fields = ["alt", "caption"]
    list_filter = ["content_type"]
    list_editable = ("ordering",)
    thumbnail = AdminThumbnail(image_field='thumb')
    fieldsets = [
        (None, {"fields": [("content_type", "object_id"), "url", "image", "ordering", ("caption", "alt")]}),
        (_("Readonly"), {
            "classes": ("collapse", "wide", "extrapretty"),
            "fields": ["webp", "image_md", "webp_md", "image_xs", "webp_xs", "thumb"]
        }),
    ]


class PictureAdminInline(GenericTabularInline):
    model = Picture
    extra = 0
    fields = ("ordering", "url", "image", ("caption", "alt"))


class PictureAdminForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'  # Keep all fields


class HistoricalFlagAdmin(admin.ModelAdmin):
    form = PictureAdminForm
    list_display = ("from_year", "to_year", "country", "title", "ordering")
    search_fields = ["title", "from_year", "country__name"]
    list_filter = ["country__name"]
    raw_id_fields = ("country",)
    list_editable = ("ordering",)
    # inlines = (PictureAdminInline, HistoricalFlagImageInline)
    inlines = (PictureAdminInline,)
    fieldsets = [
        (None, {"fields": ["country", "title", ("from_year", "to_year"), "ordering", "description"]}),
    ]


class FlagFactAdmin(admin.ModelAdmin):
    list_display = ("flag", "caption", "label", "ordering")
    search_fields = ["flag__country__name", "caption", "label"]
    # list_filter = ["flag__country__region", "flag__country"]
    raw_id_fields = ("flag",)
    list_editable = ("ordering",)
    fieldsets = [
        (None, {"fields": ["flag", "caption", ("ordering", "label"), "text", "image"]}),
    ]


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_editable = (
        "ordering",
        "is_published",
    )
    list_display = (
        # "id",
        "name",
        "slug",
        "parent",
        "ordering",
        "is_published",
    )
    # list_filter = ["parent"]
    list_filter = (ParentRegionListFilter,)
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


# class HistoricalFlagImageAdmin(admin.ModelAdmin):
#     list_display = ("flag", "image", "ordering", "alt")
#     search_fields = ["flag__country__name"]
#     # list_filter = ["country__name"]
#     readonly_fields = ['webp']
#     raw_id_fields = ("flag",)
#     fieldsets = [
#         (None, {"fields": ["flag", "img_link", ("image", "webp"), "ordering", ("caption", "alt")]}),
#     ]


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
admin.site.register(BorderCountry, BorderCountryAdmin)
admin.site.register(Picture, PictureAdmin)

# admin.site.register(HistoricalFlagImage, HistoricalFlagImageAdmin)
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
