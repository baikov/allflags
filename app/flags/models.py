from django.db import models
from django.utils.translation import gettext_lazy as _


class Seo(models.Model):
    """Abstract class for SEO fields"""

    slug = models.SlugField(max_length=100, unique=True)
    meta_title = models.CharField(
        verbose_name=_("SEO Title"), max_length=250, blank=True
    )
    meta_description = models.TextField(
        max_length=400, verbose_name=_("SEO Description"), blank=True
    )
    meta_h1 = models.CharField(verbose_name=_("SEO H1"), max_length=250, blank=True)
    is_published = models.BooleanField(
        verbose_name=_("Published"), default=False, null=False
    )
    is_index = models.BooleanField(verbose_name=_("index"), default=True, null=False)
    is_follow = models.BooleanField(verbose_name=_("follow"), default=True, null=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True
