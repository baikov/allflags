import os
from pathlib import Path

import cairosvg
import requests
from PIL import Image

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
    file_name = f"{iso2}-{from_year}-{to_year}"
    download_img(url, path, f"{file_name}.svg")
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



def svg_convert(path, file_name):
    # destination_path = f"{MEDIA_ROOT}/construction"
    # file_name, _ = svg_file.split('.', maxsplit=1)

    try:
        cairosvg.svg2png(url=f"{path}/{file_name}.svg", output_width=1000, write_to=f"{path}/{file_name}.png")
    except Exception:
        cairosvg.svg2png(
            url=f"{path}/{file_name}.svg",
            parent_width=800,
            parent_height=600,
            output_width=1000,
            write_to=f"{path}/{file_name}.png",
        )
    # im = Image.open(f"{destination_path}/{file_name}.png").convert("RGB")
    im = Image.open(f"{path}/{file_name}.png")
    im.save(
        f"{path}/{file_name}.webp",
        format="WebP",
        lossless=True,
        quality=90,
        method=6,
        minimize_size=True,
        allow_mixed=True,
    )
