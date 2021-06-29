from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from app.utils.color import Colorize


class Seo(models.Model):
    """Abstract class for SEO fields"""

    slug = models.SlugField(max_length=100, unique=True)
    seo_title = models.CharField(verbose_name=_("SEO Title"), max_length=250, blank=True)
    seo_description = models.TextField(max_length=400, verbose_name=_("SEO Description"), blank=True)
    seo_h1 = models.CharField(verbose_name=_("SEO H1"), max_length=250, blank=True)
    is_published = models.BooleanField(verbose_name=_("Published"), default=False)
    is_index = models.BooleanField(verbose_name=_("index"), default=True)
    is_follow = models.BooleanField(verbose_name=_("follow"), default=True)
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

    ru_name = models.CharField(verbose_name=_("Currency name (ru)"), max_length=100, blank=True)
    en_name = models.CharField(verbose_name=_("Currency name (en)"), max_length=100, blank=True)
    iso_num = models.CharField(verbose_name=_("Numeric code ISO 4217"), max_length=3, blank=True)
    iso_code = models.CharField(verbose_name=_("Code ISO 4217"), max_length=3)
    symbol = models.CharField(verbose_name=_("Symbol"), max_length=5, blank=True)
    countries = models.ManyToManyField("Country", related_name="currencies", verbose_name=_("Countries"), blank=True)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.ru_name} ({self.iso_code})"

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        # self.slug = self.iso_code_a2.lower()
        super(Currency, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('flags:currencies', kwargs={'iso_code': self.iso_code})


class Region(Seo, models.Model):
    name = models.CharField(verbose_name=_("Region name"), max_length=250)
    description = models.TextField(verbose_name=_("Region description"), blank=True)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self):
    #     return reverse('flags:regions', kwargs={'iso_code': self.iso_code})


class Subregion(Seo, models.Model):
    name = models.CharField(verbose_name=_("Region name"), max_length=250)
    description = models.TextField(verbose_name=_("Region description"), blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="subregion")

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


class Country(Seo, models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)
    iso_code_a2 = models.CharField(verbose_name=_("ISO code (2alpha)"), max_length=2, unique=True)
    iso_code_a3 = models.CharField(verbose_name=_("ISO code (3alpha)"), max_length=3, blank=True)
    iso_code_num = models.CharField(verbose_name=_("ISO code (numeric)"), max_length=4, blank=True)
    conventional_long_name = models.CharField(verbose_name=_("Official name"), max_length=250, blank=True)
    local_long_name = models.CharField(verbose_name=_("Official local name"), max_length=250, blank=True)
    local_short_name = models.CharField(verbose_name=_("Short local name"), max_length=250, blank=True)
    ru_capital_name = models.CharField(verbose_name=_("Capital name"), max_length=250, blank=True)
    en_capital_name = models.CharField(verbose_name="Столица на английском", max_length=250, blank=True)
    subregion = models.ForeignKey(Subregion, on_delete=models.PROTECT, related_name="countries")
    border_countries = models.ManyToManyField(
        "self",
        verbose_name=_("Border countries"),
        through="BorderCountry",
        symmetrical=False,
        related_name="border_to+",
    )
    anthem = models.URLField(verbose_name=_("Anthem URL"), max_length=250, blank=True)
    motto = models.CharField(verbose_name=_("Motto"), max_length=250, blank=True)
    ru_motto = models.CharField(verbose_name=_("Motto Ru translate"), max_length=250, blank=True)
    official_language = models.CharField(verbose_name=_("Official language"), max_length=50, blank=True)
    internet_tld = models.CharField(verbose_name=_("Internet domain"), max_length=10, blank=True)
    phone_code = models.CharField(verbose_name=_("Phone code"), max_length=10, blank=True)
    dl_imgs = models.BooleanField(verbose_name=_("Download flag images"), default=False)

    en_long_form = models.CharField(verbose_name=_("Official long name (en)"), max_length=250, blank=True)
    en_short_form = models.CharField(verbose_name=_("Short name (en)"), max_length=250, blank=True)
    # Extended country information
    ru_government_type = models.CharField(verbose_name=_("Government type (ru)"), max_length=250, blank=True)
    en_government_type = models.CharField(verbose_name=_("Government type (en)"), max_length=250, blank=True)
    ru_chief_of_state = models.CharField(verbose_name=_("Chief of state (ru)"), max_length=250, blank=True)
    en_chief_of_state = models.CharField(verbose_name=_("Chief of state (en)"), max_length=250, blank=True)
    ru_head_of_government = models.CharField(verbose_name=_("Head of government (ru)"), max_length=250, blank=True)
    en_head_of_government = models.CharField(verbose_name=_("Head of government (en)"), max_length=250, blank=True)
    area_total = models.CharField(verbose_name=_("Total area"), max_length=250, blank=True)
    area_land = models.CharField(verbose_name=_("Land area"), max_length=250, blank=True)
    area_water = models.CharField(verbose_name=_("Water area"), max_length=250, blank=True)
    coastline = models.CharField(verbose_name=_("Coastline"), max_length=250, blank=True)
    area_global_rank = models.PositiveSmallIntegerField(verbose_name=_("Area global rank"), blank=True, null=True)
    population_total = models.CharField(verbose_name=_("Population"), max_length=250, blank=True)
    population_date = models.CharField(verbose_name=_("Population stat year"), max_length=250, blank=True)
    population_global_rank = models.PositiveSmallIntegerField(
        verbose_name=_("Population global rank"), blank=True, null=True
    )
    gdp_value = models.CharField(verbose_name=_("GDP value"), max_length=250, blank=True)
    gdp_date = models.CharField(verbose_name=_("GDP stat year"), max_length=250, blank=True)
    gdp_global_rank = models.PositiveSmallIntegerField(verbose_name=_("GDP global rank"), blank=True, null=True)
    external_debt_value = models.CharField(verbose_name=_("External debt value"), max_length=250, blank=True)
    external_debt_date = models.CharField(verbose_name=_("External debt year"), max_length=250, blank=True)
    external_debt_global_rank = models.PositiveSmallIntegerField(
        verbose_name=_("External debt global rank"), blank=True, null=True
    )
    info_updated = models.CharField(verbose_name=_("Info updated date"), max_length=250, blank=True)

    ru_name_rod = models.CharField(verbose_name=_("Name (rod)"), max_length=250, blank=True)
    ru_name_dat = models.CharField(verbose_name=_("Name (dat)"), max_length=250, blank=True)
    ru_name_vin = models.CharField(verbose_name=_("Name (vin)"), max_length=250, blank=True)
    ru_name_tvo = models.CharField(verbose_name=_("Name (tvo)"), max_length=250, blank=True)
    ru_name_pre = models.CharField(verbose_name=_("Name (pre)"), max_length=250, blank=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.iso_code_a2 = self.iso_code_a2.upper()
        self.iso_code_a3 = self.iso_code_a3.upper()
        self.slug = self.iso_code_a2.lower()
        super(Country, self).save(*args, **kwargs)


class BorderCountry(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country")
    border_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="border_country")
    border = models.PositiveIntegerField(
        verbose_name=_("Border length"), help_text=_("in metres"), blank=True, null=True
    )

    class Meta:
        unique_together = ("country", "border_country")


class ColorGroup(Seo, models.Model):
    name = models.CharField(verbose_name=_("Name (ru)"), max_length=50)
    en_name = models.CharField(verbose_name=_("Name (en)"), max_length=100, blank=True)
    # ru_name_rod = models.CharField(verbose_name=_("Name (rod)"), max_length=50, blank=True)
    # ru_name_dat = models.CharField(verbose_name=_("Name (dat)"), max_length=50, blank=True)
    # ru_name_tvo = models.CharField(verbose_name=_("Name (tvo)"), max_length=50, blank=True)
    # ru_name_pre = models.CharField(verbose_name=_("Name (pre)"), max_length=50, blank=True)
    short_name = models.CharField(verbose_name=_("Short name"), max_length=50)
    description = models.TextField(verbose_name=_("Color description"), blank=True)
    colorgroup_meanings = models.TextField(verbose_name=_("Colorgroup meanings"), blank=True)

    class Meta:
        verbose_name = _("Color group")
        verbose_name_plural = _("Color groups")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("countries:color-group", kwargs={"slug": self.slug})


class Color(models.Model):

    color_group = models.ForeignKey(
        ColorGroup, verbose_name=_("Color group"), on_delete=models.PROTECT, related_name="colors"
    )
    color_meaning = models.TextField(verbose_name=_("Color meaning"), blank=True)
    hex = models.CharField(verbose_name=_("HEX"), max_length=7, unique=True, blank=True)
    rgb = ArrayField(models.SmallIntegerField(), blank=True, size=3, verbose_name=_("RGB"))
    cmyk = ArrayField(models.SmallIntegerField(), blank=True, size=4, verbose_name=_("CMYK"))
    hsl = ArrayField(models.SmallIntegerField(), blank=True, size=3, verbose_name=_("HSL"))
    pantone = models.CharField(verbose_name=_("Pantone"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Flag colors")

    def save(self, *args, **kwargs):

        if self.cmyk:
            color = Colorize(cmyk=self.cmyk)

        if self.hex:
            color = Colorize(hex=self.hex)

        if self.rgb:
            color = Colorize(self.rgb)

        self.hex = color.hex
        self.rgb = color.rgb
        self.cmyk = color.cmyk
        self.hsl = color.hsl

        super(Color, self).save(*args, **kwargs)

    def clean(self):
        if not self.rgb and not self.hex and not self.cmyk:
            raise ValidationError({"rgb": "Одно из полей должно быть заполнено"})

    def __str__(self):
        return f"{self.color_group}: #{self.hex}"

    def get_absolute_url(self):
        return reverse("countries:colors-group", kwargs={"color_group": self.color_group})


class FlagElement(Seo, models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta:
        verbose_name = _("Flag element")
        verbose_name_plural = _("Flags elements")

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = custom_slugify(FlagElement, self.name)
            self.slug = slugify(self.name)
        super(FlagElement, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class HistoricalFlag(models.Model):

#     country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='h_flags')
#     title = models.CharField(verbose_name='Заголовок', max_length=150, blank=True)
#     from_year = models.PositiveSmallIntegerField(verbose_name='Год принятия',)
#     to_year = models.PositiveSmallIntegerField(verbose_name='Год отмены',)
#     image_url = models.URLField(verbose_name='Ссылка на изображение', max_length=300)
#     image_path = FilePathField(path=f'{MEDIA_ROOT}/historical-flags', blank=True, recursive=True)
#     description = models.TextField(verbose_name='Описание', blank=True)

#     class Meta:
#         verbose_name = 'Флаг'
#         verbose_name_plural = 'Исторические флаги'

#     def __str__(self):
#         return f'{self.from_year}-{self.to_year} {self.title}'



# class FlagEmoji(Seo, models.Model):
#     flag = models.OneToOneField("MainFlag", verbose_name=_("Emoji"), on_delete=models.CASCADE, related_name="emoji")
#     unicode = models.CharField()
#     description = models.TextField(verbose_name=_("Emoji description"), blank=True)


# class FlagFact(models.Model):
#     flag = models.ForeignKey("MainFlag", verbose_name=_("Flag"), on_delete=models.CASCADE, related_name="facts")
#     text = models.TextField(verbose_name=_("Fact text"), blank=True)
#     image = models.ImageField(verbose_name=_("Fact image"), blank=True)


