import os
from pathlib import Path

import cairosvg
import requests
from PIL import Image

from config.settings.base import MEDIA_ROOT


def delete_img(file):
    os.remove(file)


def download_img(url: str, path: str, file_name: str) -> str:
    *_, ext = url.split("/")[-1].split(".")
    file = f"{path}/{file_name}.{ext}"
    Path(path).mkdir(parents=True, exist_ok=True)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",  # noqa E501
        "Accept-Language": "en-us",
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        with open(file, "wb") as f:
            f.write(r.content)
        return f"{file_name}.{ext}"
    else:
        return "status-code-not-200.png"


def get_historical_flag_img(url, from_year, to_year, country_iso2):
    iso2 = country_iso2.lower()
    path = f"{MEDIA_ROOT}/historical-flags/{iso2}"
    file_name = f"{iso2}-{from_year}-{to_year}"
    saved_file = download_img(url, path, file_name)
    # svg_convert(path, file_name)
    # return f"historical-flags/{iso2}/{file_name}"
    return f"historical-flags/{iso2}/{saved_file}"


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
            # file_name = f"{iso2}.{format}"
            download_img(url, dest, iso2)

    for format in vector:
        url = f"{cdn}/{iso2}.{format}"
        dest = f"{save_to_path}/{iso2}"
        # file_name = f"{iso2}.{format}"
        download_img(url, dest, iso2)


def get_construction_img(url, iso2):
    iso2 = iso2.lower()
    path = os.path.join(MEDIA_ROOT, "construction")
    file_name = f"{iso2}-flag-construction"

    saved_file = download_img(url, path, file_name)
    # svg_convert(path, file_name)
    # return f"construction/{file_name}"
    return f"construction/{saved_file}"


def svg_convert(file_name: str) -> None:

    path = "/".join(file_name.split("/")[:-1])
    file_name, *_, ext = file_name.split("/")[-1].split(".")
    ext = ext.lower()

    if ext == "svg":
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
    # if os.path.isfile(f"{path}/{file_name}.png") and not os.path.isfile(f"{path}/{file_name}.webp"):

    if ext == "jpg" or ext == "jpeg":
        im = Image.open(f"{path}/{file_name}.{ext}").convert("RGB")
        im.save(
            f"{path}/{file_name}.png",
            format="png",
            lossless=True,
            quality=90,
            method=6,
            minimize_size=True,
            allow_mixed=True,
        )

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
