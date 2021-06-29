import logging
import os

from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver
from utils.flag_image import get_historical_flag_img

from .models import BorderCountry, Country, HistoricalFlag

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Country)
def test_country_postsave(sender, instance, **kwargs):
    logger.info("This is a info message")
    logger.debug("This is a debug message")


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


@receiver(pre_save, sender=HistoricalFlag)
def on_create_historical_flag(sender, instance, **kwargs):
    if instance.image_url and not instance.svg_file:
        file = get_historical_flag_img(
            instance.image_url, instance.from_year, instance.to_year, instance.country.iso_code_a2
        )
        instance.svg_file = file


@receiver(post_delete, sender=HistoricalFlag)
def after_delete_historical_flag(sender, instance, **kwargs):
    if instance.svg_file:
        if os.path.isfile(instance.svg_file.path):
            os.remove(instance.svg_file.path)
