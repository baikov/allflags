import logging

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from urllib.parse import unquote

from app.utils.flag_image import (  # get_historical_flag_img, svg_convert
    convert,
    get_construction_img,
    get_h_flag_img,
    remove_historical_flag_img,
    resize,
)
from app.utils.ru_slugify import custom_slugify

from .models import (  # HistoricalFlag
    BorderCountry,
    Country,
    HistoricalFlagImage,
    MainFlag,
)
from .tasks import get_flag_img_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BorderCountry)
def create_neighbour(sender, instance, **kwargs):
    """Create symmetric record for a neighbouring country in m2m through model.

    Args:
        sender (BorderCountry): Through model for border_countries m2m field in Country model
        instance (object): has three fields (country, border_country, border)
    """
    logging.info("This is a info message")
    neighbour, _ = sender.objects.get_or_create(country=instance.border_country, border_country=instance.country)
    if neighbour.border != instance.border:
        neighbour.border = instance.border
        neighbour.save()


@receiver(post_delete, sender=BorderCountry)
def delete_neighbour(sender, instance, **kwargs):
    """Remove symmetric record for a neighbouring country in m2m through model.

    Args:
        sender (BorderCountry): Through model for border_countries m2m field in Country model
        instance (object): has three fields (country, border_country, border)
    """
    try:
        neighbour = sender.objects.get(country=instance.border_country, border_country=instance.country)
        neighbour.delete()
        logger.warning("Neighbour deleted")
    except BorderCountry.DoesNotExist:
        return


@receiver(pre_save, sender=MainFlag)
def befor_mainflag_save(sender, instance, **kwargs):
    if instance.construction_image_url and not instance.construction_image:
        main, webp = get_construction_img(
            instance.construction_image_url, instance.country.iso_code_a2
        )
        instance.construction_image = f"construction/{main}"
        instance.construction_webp = f"construction/{webp}"
    if not instance.construction_image:
        instance.construction_webp = ""

    if instance.dl_imgs:
        # country = Country.objects.get(name=instance.country)
        result = get_flag_img_task.delay(instance.country.iso_code_a2)
        task_id = result.task_id  # noqa F841
        instance.dl_imgs = False


@receiver(post_save, sender=MainFlag)
def after_create_or_update_flag(sender, instance, **kwargs):
    if kwargs["created"]:
        country = Country.objects.get(name=instance.country)
        result = get_flag_img_task.delay(country.iso_code_a2)
        task_id = result.task_id # noqa F841

    if instance.construction_image and not instance.construction_image_url and not instance.construction_webp:
        main, webp = convert(instance.construction_image.path, resize=300)
        instance.construction_image = f"construction/{main}"
        instance.construction_webp = f"construction/{webp}"
        instance.save()


@receiver(post_save, sender=Country)
def create_country_flag(sender, instance, **kwargs):
    if kwargs["created"]:
        # flag, _ = MainFlag.objects.get_or_create(country=instance)

        if instance.ru_name_rod:

            slug = custom_slugify(f'Флаг {instance.ru_name_rod}')
        else:
            slug = custom_slugify(f'Флаг {instance.name}')
        # if instance.en_short_form:
        #     slug = slugify(f'flag of {instance.en_short_form}')
        # else:
        #     slug = slugify(f'{instance.iso_code_a2} flag')

        try:
            flag = MainFlag.objects.get(country=instance)
        except MainFlag.DoesNotExist:
            flag = MainFlag(
                country=instance,
                title=f'Флаг {instance.ru_name_rod}',
                slug=slug,
            )
            flag.save()


@receiver(pre_save, sender=HistoricalFlagImage)
def historical_image_save(sender, instance, **kwargs):
    """
    Download img from url and convert it to png/jpg and webp
    """
    if instance.img_link and not instance.image:
        main, webp = get_h_flag_img(
            instance.img_link, instance.flag.country.iso_code_a2
        )
        instance.image = f"historical-flags/{instance.flag.country.iso_code_a2.lower()}/{main}"
        instance.webp = f"historical-flags/{instance.flag.country.iso_code_a2.lower()}/{webp}"
        instance.img_link = unquote(instance.img_link)


@receiver(post_save, sender=HistoricalFlagImage)
def resize_image(sender, instance, **kwargs):
    iso2 = instance.flag.country.iso_code_a2.lower()
    if instance.image:
        resize(instance.image.path, iso2, sizes=(600, 300))
    if instance.webp:
        resize(instance.webp.path, iso2, sizes=(600, 300))
    if instance.image and kwargs["created"]:
        main, webp = convert(instance.image.path)
        instance.image = f"historical-flags/{instance.flag.country.iso_code_a2.lower()}/{main}"
        instance.webp = f"historical-flags/{instance.flag.country.iso_code_a2.lower()}/{webp}"
        instance.save()


@receiver(post_delete, sender=HistoricalFlagImage)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        remove_historical_flag_img(instance.image.path)
    if instance.webp:
        remove_historical_flag_img(instance.webp.path)


"""
@receiver(m2m_changed, sender=BorderCountry)
def m2m_test(sender, instance, **kwargs):
    print("m2m change!")
    action = kwargs.pop("action", None)
    if action == "post_add":
        print("m2m postsave!")
    if action == "post_remove":
        print("m2m postdelete!")


@receiver(m2m_changed, sender=Country.border_countries.through)
def m2m_test_2(sender, instance, **kwargs):
    print("m2m change!")
    action = kwargs.pop("action", None)
    if action == "post_add":
        print("m2m postsave!")
    if action == "post_remove":
        print("m2m postdelete!")
"""
