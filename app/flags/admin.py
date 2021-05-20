from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Currency, Region, Subregion


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("ru_name", "iso_code")
    search_fields = ["ru_name", "iso_code"]
    # filter_horizontal = ("countries",)


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ["name"]
    fieldsets = [
        (None, {"fields": ["name", "slug", "description"]}),
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


class SubregionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "region")
    search_fields = ["name", "region"]
    fieldsets = [
        (None, {"fields": ["region", "name", "slug", "description"]}),
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
admin.site.register(Subregion, SubregionAdmin)
