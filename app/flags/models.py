from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Seo(models.Model):
    """Abstract class for SEO fields"""

    slug = models.SlugField(max_length=100, unique=True)
    meta_title = models.CharField(verbose_name=_("SEO Title"), max_length=250, blank=True)
    meta_description = models.TextField(max_length=400, verbose_name=_("SEO Description"), blank=True)
    meta_h1 = models.CharField(verbose_name=_("SEO H1"), max_length=250, blank=True)
    is_published = models.BooleanField(verbose_name=_("Published"), default=False, null=False)
    is_index = models.BooleanField(verbose_name=_("index"), default=True, null=False)
    is_follow = models.BooleanField(verbose_name=_("follow"), default=True, null=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class PublishedQuerySet(models.QuerySet):
    """Return only published elements"""

    def published(self):
        return self.filter(is_published=True)


class Currency(models.Model):
    """Model for countries currency with m2m rel"""

    ru_name = models.CharField(verbose_name=_("Currency name (ru)"), max_length=250, blank=True)
    en_name = models.CharField(verbose_name=_("Currency name (en)"), max_length=250, blank=True)
    iso_num = models.CharField(verbose_name=_("Numeric code ISO 4217"), max_length=250, blank=True)
    iso_code = models.CharField(verbose_name=_("Code ISO 4217"), max_length=250, blank=True)
    symbol = models.CharField(verbose_name=_("Symbol"), max_length=5, blank=True)
    countries = models.ManyToManyField("Country", related_name="currencies", verbose_name=_("Countries"), blank=True)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.ru_name} ({self.iso_code})"

    # def get_absolute_url(self):
    #     return reverse('flags:currencies', kwargs={'iso_code': self.iso_code})


class Region(Seo, models.Model):
    name = models.CharField(verbose_name=_("Region name"), max_length=250)
    description = models.TextField(verbose_name=_("Region description"), blank=True)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name})"

    # def get_absolute_url(self):
    #     return reverse('flags:regions', kwargs={'iso_code': self.iso_code})


class SubRegion(Seo, models.Model):
    name = models.CharField(verbose_name=_("Region name"), max_length=250)
    description = models.TextField(verbose_name=_("Region description"), blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="subregion")

    class Meta:
        verbose_name = _("Subregion")
        verbose_name_plural = _("Subregions")

    def __str__(self):
        return f"{self.name} ({self.region})"

    # def get_absolute_url(self):
    #     return reverse('flags:regions', kwargs={'iso_code': self.iso_code})

    @property
    def get_region(self):
        """Rreturn name of parent region"""
        return self.region
