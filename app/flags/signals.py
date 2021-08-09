import logging
import os

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from app.utils.flag_image import (
    get_construction_img,
    get_historical_flag_img,
    svg_convert,
)
from app.utils.ru_slugify import custom_slugify

from .models import BorderCountry, Country, HistoricalFlag, MainFlag
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


@receiver(pre_save, sender=HistoricalFlag)
def before_create_historical_flag(sender, instance, **kwargs):
    """Download svg image from link in image_url field and save file in svg_file field

    Args:
        sender (HistoricalFlag): Model
        instance (object): has image_url as models.URLField and svg_image as models.FileField
    """
    if instance.image_url and not instance.svg_file:
        file = get_historical_flag_img(
            instance.image_url, instance.from_year, instance.to_year, instance.country.iso_code_a2
        )
        instance.svg_file = file


@receiver(post_save, sender=HistoricalFlag)
def after_create_historical_flag(sender, instance, **kwargs):
    """
    Converting uploaded or downloaded svg file into png and webp
    """
    if instance.svg_file:
        svg_convert(instance.svg_file.path)


@receiver(post_delete, sender=HistoricalFlag)
def after_delete_historical_flag(sender, instance, **kwargs):
    if instance.svg_file:
        if os.path.isfile(instance.svg_file.path):
            os.remove(instance.svg_file.path)


@receiver(pre_save, sender=MainFlag)
def befor_mainflag_save(sender, instance, **kwargs):
    if instance.construction_image_url and not instance.construction_image_file:
        file = get_construction_img(
            instance.construction_image_url, instance.country.iso_code_a2
        )
        # instance.construction_image_file = f"{file}.svg"
        instance.construction_image_file = file

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

    if instance.construction_image_file:
        svg_convert(instance.construction_image_file.path)
        # instance.construction_image = f"{}.png"


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
