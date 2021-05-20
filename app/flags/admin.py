from django.contrib import admin
from .models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("ru_name", "iso_code")
    search_fields = ["ru_name", "iso_code"]
    filter_horizontal = ("countries",)


admin.site.register(Currency, CurrencyAdmin)
