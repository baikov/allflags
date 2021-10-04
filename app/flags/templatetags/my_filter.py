from django import template

from config.settings.base import MEDIA_URL

register = template.Library()


@register.filter()
def get_name(object, field):
    verbose_name = object._meta.get_field(field).verbose_name
    return verbose_name


@register.filter()
def in_km(field):
    width = f"{field/1000} км"
    return width


@register.filter()
def get_img_path(object, size=""):
    object = object.lower()
    if size:
        return f"{MEDIA_URL}national-flags/{object}/{size}/{object}-{size}"
    else:
        return f"{MEDIA_URL}national-flags/{object}/{object}"


@register.filter()
def ru_count(object, case="i"):
    numerals = {
        "1": {"i": "один", "r": "одного", "d": "одному", "v": "один", "t": "одним", "p": "одном"},
        "2": {"i": "два", "r": "двух", "d": "двум", "v": "два", "t": "двумя", "p": "двух"},
        "3": {"i": "три", "r": "трех", "d": "трем", "v": "три", "t": "тремя", "p": "трех"},
        "4": {"i": "четыре", "r": "четырёх", "d": "четырём", "v": "четыре", "t": "четырьмя", "p": "четырёх"},
        "5": {"i": "пять", "r": "пяти", "d": "пяти", "v": "пять", "t": "пятью", "p": "пяти"},
        "6": {"i": "шесть", "r": "шести", "d": "шести", "v": "шесть", "t": "шестью", "p": "шести"},
        "7": {"i": "семь", "r": "семи", "d": "семи", "v": "семь", "t": "семью", "p": "семи"},
        "8": {"i": "восемь", "r": "восьми", "d": "восьми", "v": "восемь", "t": "восьмью", "p": "восьми"},
    }

    return numerals[str(object)][case]


@register.filter()
def adjective(object, case="i"):
    dictionary = {
        "ru": {
            "i": "Российский",
            "r": "Российского",
            "d": "Российскому",
            "v": "Российский",
            "t": "Российским",
            "p": "Российском",
        },
    }
    if str(object) in dictionary.keys():
        return dictionary[str(object).lower()][case]
    else:
        return "Государственный"


'''
@register.filter()
def resize(object, size="600"):
    name = object.path.split("/")[-1]
    iso2 = object.path.split("/")[-2]
    return f"{MEDIA_URL}historical-flags/resized/{iso2}/{size}/{name}"
'''
