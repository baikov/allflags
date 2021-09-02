import io
import os
import re
import urllib

import cairosvg
from defusedxml.common import EntitiesForbidden
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from config.settings.base import MEDIA_ROOT


def download_image(url: str) -> SimpleUploadedFile:
    path, file_name = os.path.split(url)
    name, ext = os.path.splitext(file_name)
    ext = ext.lower()

    file = io.BytesIO(urllib.request.urlopen(url).read())

    if ext == ".svg":
        new = io.BytesIO()
        try:
            cairosvg.svg2png(file_obj=file, output_width=800, write_to=new)
        except EntitiesForbidden:
            rgx_list = [r"<!ENTITY .*?>", r"xmlns=.*?;\"", r"xmlns:xlink=.*?;\""]
            file.seek(0)
            file_str = file.read().decode("UTF-8")
            for rgx_match in rgx_list:
                file_str = re.sub(rgx_match, "", file_str)
            file = io.BytesIO(file_str.encode("UTF-8"))
            cairosvg.svg2png(file_obj=file, output_width=800, write_to=new)
        except Exception as e:
            return e
        new.seek(0)
        file = new
        ext = ".png"

    img = Image.open(file)
    format = img.format
    width, height = img.size
    width, height = scale_dimensions(width, height, longest_side=800)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(file, format=format)
    file.seek(0)
    return SimpleUploadedFile(f"{name}{ext}", file.read())


def scale_dimensions(width: int, height: int, longest_side: int) -> tuple:
    ratio = width / height
    if ratio > 1:
        return longest_side, int(longest_side / ratio)
    # Portrait
    else:
        return int(longest_side * ratio), longest_side


def img_path_by_flag_type(instance, filename) -> str:
    """Determines the path depending on the calling model. Uses in property upload_to of FileField.

    Args:
        instance (): instanse of callable model (MainFlag or HistoricalFlag)
        filename (str): name of the uploading file

    Returns:
        str: path for saving uploaded file
    """
    iso2 = instance.flag.country.iso_code_a2.lower()
    # folder = f"historical-flags/{iso2}"
    if str(instance._meta.verbose_name) == "Main flag image":
        folder = f"national-flags/{iso2}"
    elif str(instance._meta.verbose_name) == "Historical flag image":
        folder = f"historical-flags/{iso2}"
    return os.path.join(folder, filename)


def historical_flag_img_file_path(instance, filename):
    ext = filename.split(".")[-1]
    iso2 = instance.country.iso_code_a2.lower()
    path = f"historical-flags/{iso2}"
    filename = f"{iso2}-{instance.from_year}-{instance.to_year}.{ext}"

    if os.path.isfile(os.path.join(MEDIA_ROOT, path, filename)):
        os.remove(os.path.join(MEDIA_ROOT, path, filename))

    return os.path.join(path, filename)
