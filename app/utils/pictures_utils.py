import io
import logging
import os
import re

import cairosvg
import urllib3
from defusedxml.common import EntitiesForbidden
from django.core.files.images import ImageFile
from PIL import Image

# from app.utils.ru_slugify import custom_slugify

logger = logging.getLogger(__name__)


def split_url(url: str) -> tuple:
    path, file_name = os.path.split(url)
    name, ext = os.path.splitext(file_name)
    ext = ext.lower()

    return (path, name, ext)


def url_is_ok(url: str) -> bool:
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return r.status == 200


def get_file_to_bytesio(url: str = None, local_file=None) -> io.BytesIO:
    if url:
        logger.info(url)
        path, name, ext = split_url(url)
        http = urllib3.PoolManager()
        r = http.request("GET", url)
        if r.status == 200:
            file = io.BytesIO(r.data)
            file.name = name
            file.ext = ext
        else:
            return "not 200"

    elif local_file:
        path, name, ext = split_url(local_file.path)
        file = io.BytesIO(local_file.read())
        file.name = name
        file.ext = ext
    else:
        file = None
        file.error = "miss url or local file"

    return file


def convert_and_compress_image(file, longest_side: int = 1200) -> ImageFile:
    logger.warn(file)
    ext = file.ext
    name = file.name

    if ext == ".svg":
        new = io.BytesIO()
        try:
            cairosvg.svg2png(file_obj=file, output_width=longest_side, write_to=new)
        except EntitiesForbidden:
            rgx_list = [r"<!ENTITY .*?>", r"xmlns=.*?;\"", r"xmlns:xlink=.*?;\""]
            file.seek(0)
            file_str = file.read().decode("UTF-8")
            for rgx_match in rgx_list:
                file_str = re.sub(rgx_match, "", file_str)
            file = io.BytesIO(file_str.encode("UTF-8"))
            cairosvg.svg2png(file_obj=file, output_width=longest_side, write_to=new)
        except Exception as e:
            return e
        new.seek(0)
        file = new
        ext = ".png"

    img = Image.open(file)
    format = img.format
    width, height = img.size
    width, height = scale_dimensions(width, height, longest_side=longest_side)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(file, format=format)
    file.seek(0)

    return ImageFile(file=file, name=f"{name}{ext}")


def scale_dimensions(width: int, height: int, longest_side: int) -> tuple:
    ratio = width / height
    if ratio > 1:
        return longest_side, int(longest_side / ratio)
    # Portrait
    else:
        return int(longest_side * ratio), longest_side


def img_path_by_model(instance, filename) -> str:
    """Determines the path depending on the calling model. Uses in property upload_to of FileField.

    Args:
        instance (): instanse of callable model (MainFlagPicture or HistoricalFlagPicture)
        filename (str): name of the uploading file

    Returns:
        str: path for saving uploaded file
    """

    logger.info(str(instance._meta.verbose_name))  # instance.__class__ or instance.__name__

    # verbose_name = str(instance.content_type.model_class()._meta.verbose_name)
    verbose_name = str(instance._meta.verbose_name)

    if verbose_name == "File":  # or verbose_name == "Файл"
        path = f"files/{instance.flag.country.iso_code_a2}/"
        return os.path.join(path, filename)
    elif verbose_name == "Historical picture":
        return os.path.join("pictures/", filename)
    else:
        # return os.path.join(f"{custom_slugify(verbose_name)}/", filename)
        return filename


# def download_image(url: str) -> SimpleUploadedFile:
#     path, file_name = os.path.split(url)
#     name, ext = os.path.splitext(file_name)
#     ext = ext.lower()

#     file = io.BytesIO(urllib.request.urlopen(url).read())

#     if ext == ".svg":
#         new = io.BytesIO()
#         try:
#             cairosvg.svg2png(file_obj=file, output_width=800, write_to=new)
#         except EntitiesForbidden:
#             rgx_list = [r"<!ENTITY .*?>", r"xmlns=.*?;\"", r"xmlns:xlink=.*?;\""]
#             file.seek(0)
#             file_str = file.read().decode("UTF-8")
#             for rgx_match in rgx_list:
#                 file_str = re.sub(rgx_match, "", file_str)
#             file = io.BytesIO(file_str.encode("UTF-8"))
#             cairosvg.svg2png(file_obj=file, output_width=800, write_to=new)
#         except Exception as e:
#             return e
#         new.seek(0)
#         file = new
#         ext = ".png"

#     img = Image.open(file)
#     format = img.format
#     width, height = img.size
#     width, height = scale_dimensions(width, height, longest_side=800)
#     img = img.resize((width, height), Image.ANTIALIAS)
#     img.save(file, format=format)
#     file.seek(0)
#     return SimpleUploadedFile(f"{name}{ext}", file.read())
