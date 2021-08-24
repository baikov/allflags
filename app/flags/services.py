import os

from config.settings.base import MEDIA_ROOT


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
