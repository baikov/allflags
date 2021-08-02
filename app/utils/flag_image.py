import os
from pathlib import Path

import requests

from config.settings.base import MEDIA_ROOT


def delete_img(file):
    os.remove(file)


def download_img(url, path, name):
    file = f"{path}/{name}"
    Path(path).mkdir(parents=True, exist_ok=True)
    r = requests.get(url)
    # print(f'{url}: {r.status_code}')
    with open(file, "wb") as f:
        f.write(r.content)


def get_historical_flag_img(url, from_year, to_year, country_iso2):
    iso2 = country_iso2.lower()
    path = f"{MEDIA_ROOT}/historical-flags/{iso2}"
    file_name = f"{iso2}-{from_year}-{to_year}.svg"
    download_img(url, path, file_name)

    return f"historical-flags/{iso2}/{file_name}"


def get_flag_img(iso2):
    sizes = [
        "w20",
        "w40",
        "w80",
        "w160",
        "w320",
        "w640",
        "w1280",
        "w2560",
        "h20",
        "h24",
        "h40",
        "h60",
        "h80",
        "h120",
        "h240",
    ]
    bitmap = ["png", "jpg", "webp"]
    vector = ["svg", "ai", "pdf", "eps"]
    cdn = "https://flagcdn.com"
    save_to_path = f"{MEDIA_ROOT}/national-flags"
    Path(save_to_path).mkdir(parents=True, exist_ok=True)
    iso2 = iso2.lower()
    for format in bitmap:
        for size in sizes:
            url = f"{cdn}/{size}/{iso2}.{format}"
            dest = f"{save_to_path}/{iso2}/{size}"
            file_name = f"{iso2}.{format}"
            download_img(url, dest, file_name)

    for format in vector:
        url = f"{cdn}/{iso2}.{format}"
        dest = f"{save_to_path}/{iso2}"
        file_name = f"{iso2}.{format}"
        download_img(url, dest, file_name)
