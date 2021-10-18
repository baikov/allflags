import logging
from datetime import date, datetime

from django.core.files import File
from django.db.models import Count, Max
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from app.utils.pictures_utils import get_file_to_bytesio

from .models import (
    BorderCountry,
    ColorGroup,
    DownloadablePictureFile,
    DownloadablePictureFilePreview,
    FlagElement,
    HistoricalFlag,
    MainFlag,
)

# from config.settings.base import MEDIA_ROOT

logger = logging.getLogger(__name__)


# ORM queries for flag detail
def flag_last_modified(reqest, flag_slug):
    last_mod = MainFlag.objects.get(slug=flag_slug).updated_date
    # last_mod = datetime.combine(flag.updated_date, datetime.min.time())
    return last_mod


def get_flag_or_404(request, flag_slug: str) -> MainFlag:
    if request.user.is_superuser:
        flag = get_object_or_404(
            MainFlag.objects
            .select_related("country", "country__region")
            .prefetch_related("elements", "facts"),
            slug=flag_slug,
        )
    else:
        flag = get_object_or_404(
            MainFlag.objects
            .select_related("country", "country__region")
            .prefetch_related("elements", "facts"),
            slug=flag_slug,
            is_index=True,
            is_published=True,
        )

    return flag


def get_files(flag_id):
    files = (
        DownloadablePictureFilePreview.objects
        .prefetch_related("files")
        .filter(flag__id=flag_id)
        .filter(is_show_on_detail=True)
    )
    return files


def get_historical_flags(iso2: str) -> QuerySet:

    return HistoricalFlag.objects.prefetch_related("images").filter(country__iso_code_a2=iso2)


def get_neighbours(country_id: int) -> QuerySet:
    return (
        BorderCountry.objects
        .select_related("border_country")
        .filter(country__id=country_id)
        # .prefetch_related("")
    )


def get_neighbours_flags(neighbours_id: list[int]) -> QuerySet:
    return (
        MainFlag.objects.select_related("country")
        .prefetch_related("downloads")
        .filter(country__id__in=neighbours_id)
    )


def get_flags_with_same_colors(flag_id: int, same_color_groups: list) -> QuerySet:
    # flags = (
    #     MainFlag.objects.select_related("country")
    #     .prefetch_related("downloads")
    #     .filter(colors_set__color_group__slug__in=same_color_groups)
    #     .exclude(id=flag_id).distinct()
    # )
    # for color in same_color_groups:
    #     # logger.info(color["color_group__slug"])
    #     flags = flags.filter(colors_set__color_group__slug=color["color_group__slug"])
    #     # logger.info(flags)
    result = []
    colors = set([color["color_group__slug"] for color in same_color_groups])
    flags = (
        MainFlag.objects
        .select_related("country")
        .prefetch_related("downloads", "colors_set", "colors_set__color_group")
        .filter(colors_set__color_group__slug__in=colors)  # Why it works?!
        .exclude(id=flag_id)
        .distinct()
    )
    for elem in flags.all():
        col = set()
        for color in elem.colors_set.all():
            if color.is_main is True:
                col.add(color.color_group.slug)
        if col == colors:
            result.append(elem)
    # logger.info(flag)
    # logger.info(colors)
    # logger.info(flags)
    # logger.info(result)
    return result


def get_flag_age(adopted_date: date) -> int:
    if adopted_date:
        return int(datetime.now().strftime("%Y")) - int(adopted_date.strftime("%Y"))
    else:
        return 0


def get_color_adjectives(main_colors) -> str:
    # colors = ColorGroup.objects.filter(slug__in=same_color_groups)
    adj = ""
    if len(main_colors) > 1:
        for i in range(len(main_colors) - 1):
            adj += str(main_colors[i].color_group.short_name).lower()
            adj += "-"
        adj += str(main_colors[len(main_colors) - 1].color_group.name).lower()
    else:
        adj = main_colors[0].color_group.name
    return adj


def get_img_from_cdn(flag_id, iso2):
    bitmap = [".png", ".jpg", ".webp"]
    vector = [".svg", ".ai", ".pdf", ".eps"]
    cdn = "https://flagcdn.com"
    # https://flagcdn.com/w640/ru.png
    preview_url = f"{cdn}/w640/{iso2.lower()}.png"
    # url = f"{cdn}/{size}/{iso2}.{format}"
    preview_file = get_file_to_bytesio(url=preview_url)
    flag = MainFlag.objects.get(id=flag_id)
    try:
        img = DownloadablePictureFilePreview.objects.get(
            flag=flag,
            is_main=True
        )
    except DownloadablePictureFilePreview.DoesNotExist:
        img = DownloadablePictureFilePreview(
            flag=flag,
            image=File(preview_file, f"files/{iso2.lower()}/{preview_file.name}-preview{preview_file.ext}"),
            is_published=True,
            is_show_on_detail=True,
            is_main=True,
            description="<p>Данное изображение флага было взято с википедии и сконвертировано в несколько форматов.</p>"
        )
        img.save()

    files = DownloadablePictureFile.objects.filter(picture=img)
    existing_file_types = []
    for file in files:
        existing_file_types.append(file.get_type)

    for ext in set(bitmap)-set(existing_file_types):  # noqa E226
        dl_file_url = f"{cdn}/w2560/{iso2.lower()}{ext}"
        dl_file = get_file_to_bytesio(url=dl_file_url)
        file = DownloadablePictureFile(
            picture=img,
            file=File(dl_file, f"{iso2.lower()}/{dl_file.name}{dl_file.ext}"),
        )
        file.save()

    for ext in set(vector)-set(existing_file_types):  # noqa E226
        dl_file_url = f"{cdn}/{iso2.lower()}{ext}"
        dl_file = get_file_to_bytesio(url=dl_file_url)
        file = DownloadablePictureFile(
            picture=img,
            file=File(dl_file, f"{iso2.lower()}/{dl_file.name}{dl_file.ext}"),
        )
        file.save()


def make_mainflag_meta(meta_data: dict) -> tuple:
    flag = meta_data["flag"]
    colors_adj = meta_data["colors_adj"]
    main_colors = meta_data["main_colors"]
    colors_count = len(main_colors)

    # Generate descr
    if not flag.seo_description:
        if colors_count == 1:
            colors_txt = f"Единственный цвет флага: {main_colors[0].color_group.lower()}."
        else:
            cols = ", ".join(color.color_group.name.lower() for color in main_colors)
            if colors_count > 4:
                rod = "цветов"
            else:
                rod = "цвета"
            count_text = ("Нет", "Один", "Два", "Три", "Четыре", "Пять", "Шесть", "Семь", "Восемь")
            colors_txt = f"{count_text[colors_count]} основных {rod} флага: {cols}."

        if flag.elements:
            el_name = ", ".join(elem.name.lower() for elem in flag.elements.all())
            elem = f"Элементы флага: {el_name}."

        if flag.adopted_date:
            date = f"Флаг страны {flag.country.name} был утвержден {flag.adopted_date.strftime('%d.%m.%Y')}."
        descr = f"Государственный флаг {flag.country.ru_name_rod} {flag.emoji} - это \
            прямоугольное полотнище с пропорциями сторон {flag.proportion}. \
            {colors_txt} {elem} {date}"
    else:
        descr = flag.seo_description
    # End descr

    if not flag.seo_title:
        flag_name = flag.name if flag.name else "флаг"
        title = f"Флаг {flag.country.ru_name_rod} {flag.emoji} ({colors_adj} {flag_name}) - история, цвета, описание"
    else:
        title = flag.seo_title

    return title, descr


# ORM for colors
def color_last_modified(reqest, slug):
    group = ColorGroup.objects.get(slug=slug)
    # colors_updated_date = group.colors.all().aggregate(Max("updated_date"))
    # last_mod = max(group.updated_date, colors_updated_date["updated_date__max"])
    # logger.info(f"Group: {group.updated_date}")
    # logger.info(f"Colors: {colors_updated_date['updated_date__max']}")
    # logger.info(last_mod)
    # .strftime('%a, %d %b %Y %H:%M:%S GMT')
    last_mod = group.updated_date
    return last_mod


def get_colorgroup_or_404(request, slug: str) -> ColorGroup:
    if request.user.is_superuser:
        group = get_object_or_404(
            ColorGroup.objects.prefetch_related("colors", "colors__flag"),
            slug=slug,
        )
    else:
        group = get_object_or_404(
            ColorGroup.objects.prefetch_related("colors", "colors__flag"),
            slug=slug,
            is_index=True,
            is_published=True,
        )

    return group


def make_colorgroup_meta(meta_data: dict) -> tuple:
    group = meta_data["group"]
    flags_count = meta_data["flags_count"]
    group_names = {
        "Красный": "красным",
        "Белый": "белым",
        "Синий": "синим",
        "Зеленый": "зеленым",
        "Голубой": "голубым",
        "Розовый": "розовым",
        "Бордовый": "бордовым",
        "Коричневый": "коричневым",
        "Черный": "черным",
        "Фиолетовый": "фиолетовым",
        "Желтый": "желтым",
        "Оранжевый": "оранжевым",
    }

    if not group.seo_description:
        descr = f"""{group.name} цвет встречается на флагах {flags_count} стран мира и
        имеет различные значения и символизм.
        Мы собрали полный список флагов с {group_names[group.name]} цветом, а так же точные значения цветов
        в форматах hex, rgb, hls, cmyk."""
    else:
        descr = group.seo_description

    if not group.seo_title:
        title = f"""{group.name} цвет на флагах стран и его значение -
        список флагов с {group_names[group.name]} цветом | AllFlags.ru"""
    else:
        title = group.seo_title

    return title, descr


# ORM for elements
def element_last_modified(reqest, slug):
    element = FlagElement.objects.prefetch_related("flags_with_elem").get(slug=slug)
    flags_updated_date = element.flags_with_elem.all().aggregate(Max("updated_date"))
    last_mod = max(element.updated_date, flags_updated_date["updated_date__max"])
    # .strftime('%a, %d %b %Y %H:%M:%S GMT')

    return last_mod


def get_element_or_404(request, slug) -> FlagElement:
    if request.user.is_superuser:
        element = get_object_or_404(
            FlagElement.objects.prefetch_related("flags_with_elem", "flags_with_elem__downloads"),
            slug=slug,
        )
    else:
        element = get_object_or_404(
            FlagElement.objects.prefetch_related("flags_with_elem", "flags_with_elem__downloads"),
            slug=slug,
            is_index=True,
            is_published=True,
        )

    return element


def get_all_elements(request) -> QuerySet:
    if request.user.is_superuser:
        elements = (
            FlagElement.objects
            .annotate(flags_count=Count("flags_with_elem"))
            .all()
            .order_by("-flags_count")
        )
    else:
        elements = (
            FlagElement.objects
            .annotate(flags_count=Count("flags_with_elem"))
            .filter(flags_count__gt=0, is_index=True, is_published=True)
            .order_by("-flags_count")
        )

    return elements


'''
# Moved to model as method
def get_emoji(iso2: str) -> str:
    OFFSET = ord("🇦") - ord("A")
    return chr(ord(iso2[0]) + OFFSET) + chr(ord(iso2[1]) + OFFSET)
'''
