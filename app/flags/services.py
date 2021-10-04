from datetime import date, datetime

from django.core.files import File
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from app.utils.pictures_utils import get_file_to_bytesio

    DownloadablePictureFile,
    DownloadablePictureFilePreview,
# from config.settings.base import MEDIA_ROOT


# ORM queries for flag detail
def get_flag_or_404(request, flag_slug: str) -> MainFlag:
    if request.user.is_superuser:
        flag = get_object_or_404(
            MainFlag.objects.select_related("country", "country__region").prefetch_related("elements", "facts"),
            slug=flag_slug,
        )
    else:
        flag = get_object_or_404(
            MainFlag.objects.select_related("country", "country__region").prefetch_related("elements", "facts"),
            slug=flag_slug,
            is_index=True,
            is_published=True,
        )

    return flag


def get_emoji(iso2: str) -> str:
    OFFSET = ord("🇦") - ord("A")
    return chr(ord(iso2[0]) + OFFSET) + chr(ord(iso2[1]) + OFFSET)


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
        .filter(country__id__in=neighbours_id)
    )


def get_flags_with_same_colors(flag_id: int, same_color_groups: list) -> QuerySet:
    return (
        MainFlag.objects.select_related("country")
        .filter(colors_set__color_group__slug__in=same_color_groups)
        .exclude(id=flag_id).distinct()
    )


def get_flag_age(adopted_date: date) -> int:
    if adopted_date:
        return int(datetime.now().strftime("%Y")) - int(adopted_date.strftime("%Y"))
    else:
        return 0


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
            is_main=True
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
