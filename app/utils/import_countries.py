import json
import os

from app.flags.models import BorderCountry, Country, Region
from config.settings.base import MEDIA_ROOT

# from django.utils.text import slugify

COUNTRY_FILE = "test.json"


def create_countries(file):
    print("+[Success] Start importing countries:")
    with open(os.path.join(MEDIA_ROOT, file), "r") as f:
        country_json = json.load(f)
        print(f"+[Success] File {COUNTRY_FILE} successfully opened!")
    # Get data from json
    for code, data in country_json.items():
        print(f"+[Success] Code {code} in loop")
        try:
            region = Region.objects.get(name=data["exact_region"])
        except Region.DoesNotExist:
            print(f'![Error] Region {data["exact_region"]} doesn\'t exist')

        iso_code_a2 = data["iso_2"]
        # if iso_code_a2 == 'AE':
        if iso_code_a2:
            print(f"+[Success] Enter into {iso_code_a2} condition")
            # country, created = Country.objects.get_or_create(iso_code_a2=iso_code_a2)
            try:
                country = Country.objects.get(iso_code_a2=iso_code_a2)
                print(f"+[Warn] Country {country} exist!")
            except Country.DoesNotExist:
                country = Country(
                    name=data["name"]["ru_short_form"],
                    conventional_long_name=data["name"]["ru_long_form"],
                    local_long_name=data["name"]["local_long_form"],
                    local_short_name=data["name"]["local_short_form"],
                    en_long_form=data["name"]["en_long_form"],
                    en_short_form=data["name"]["en_short_form"],
                    ru_name_rod=data["name"]["ru_name_rod"],
                    ru_name_dat=data["name"]["ru_name_dat"],
                    ru_name_vin=data["name"]["ru_name_vin"],
                    ru_name_tvo=data["name"]["ru_name_tvo"],
                    ru_name_pre=data["name"]["ru_name_pre"],
                    region=region,
                    ru_capital_name=data["ru_capital"],
                    en_capital_name=data["capital"],
                    anthem=data["anthem_audio_url"],
                    internet_tld=data["internet_tld"],
                    phone_code=data["phone_code"],
                    iso_code_a2=data["iso_2"],
                    iso_code_a3=data["iso_3"],
                    iso_code_num=data["iso_num"],
                    ru_government_type=data["ru_government_type"],
                    en_government_type=data["en_government_type"],
                    ru_chief_of_state=data["ru_chief_of_state"],
                    en_chief_of_state=data["en_chief_of_state"],
                    ru_head_of_government=data["ru_head_of_government"],
                    en_head_of_government=data["en_head_of_government"],
                    area_total=data["area"]["total"] if data["area"]["total"] else 0,
                    area_land=data["area"]["land"] if data["area"]["land"] else 0,
                    area_water=data["area"]["water"] if data["area"]["water"] else 0,
                    coastline=data["coastline"] if data["coastline"] else 0,
                    area_global_rank=data["area"]["global_rank"] if data["area"]["global_rank"] else 9000,
                    population_total=data["population"]["total"] if data["population"]["total"] else 0,
                    population_date=data["population"]["date"],
                    population_global_rank=data["population"]["global_rank"]
                    if data["population"]["global_rank"]
                    else 9000,
                    gdp_value=data["gdp"]["value"] if data["gdp"]["value"] else 0,
                    gdp_date=data["gdp"]["date"],
                    gdp_global_rank=data["gdp"]["global_rank"] if data["gdp"]["global_rank"] else 9000,
                    external_debt_value=data["external_debt"]["value"] if data["external_debt"]["value"] else 0,
                    external_debt_date=data["external_debt"]["date"],
                    external_debt_global_rank=data["external_debt"]["global_rank"]
                    if data["external_debt"]["global_rank"]
                    else 9000,
                    info_updated=data["updated"],
                )
                country.save()
                print(f"+[Success] Country {country} created!")


def add_border_countries(file):
    with open(os.path.join(MEDIA_ROOT, file), "r") as f:
        neighbours_json = json.load(f)
        print(f"+[Success] File {file} successfully opened!")
    # Get data from json
    for record in neighbours_json:
        print(f"+[Success] {record[0]} - {record[1]} - {record[2]}")
        try:
            country = Country.objects.get(iso_code_a2=record[0])
        except Country.DoesNotExist:
            continue

        try:
            neighbour = Country.objects.get(iso_code_a2=record[1])
        except Country.DoesNotExist:
            continue

        try:
            neighbours_record = BorderCountry.objects.get(country=country, border_country=neighbour)
            neighbours_record.border = int(record[2])
            neighbours_record.save()
            print(f"+[Warn!] Pair {country}-{neighbour} exist!")
        except BorderCountry.DoesNotExist:
            neighbours_record = BorderCountry(country=country, border_country=neighbour, border=int(record[2]))
            neighbours_record.save()
            print(f"+[Success] Record {country}-{neighbour} successfully saved!")
