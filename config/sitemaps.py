from django.contrib.sitemaps import Sitemap
from django.urls.base import reverse

from app.flags.models import ColorGroup, FlagElement, MainFlag, Region


class MainFlagSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return MainFlag.objects.filter(is_index__exact=True, is_published__exact=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj) -> str:
        return reverse('flags:flag-detail', args=[obj.slug])


class RegionSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Region.objects.filter(is_index__exact=True, is_published__exact=True)

    def lastmod(self, obj):
        return obj.updated_date


class FlagElementSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return FlagElement.objects.filter(is_index__exact=True, is_published__exact=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj) -> str:
        return reverse('flags:element-detail', args=[obj.slug])


class ColorGroupSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ColorGroup.objects.filter(is_index__exact=True, is_published__exact=True)
        # return ColorGroup.objects.all().distinct('color_group')

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj) -> str:
        return reverse('flags:color-detail', args=[obj.slug])
        # return reverse('flags:colors-count', args=[3])


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['about', 'flags:regions-list', 'flags:colors-list', 'flags:elements-list']

    def location(self, item):
        return reverse(item)
