import logging
import os
import shutil

from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from imagekit.utils import get_cache

from app.flags.models import (  # HistoricalFlag,
    BorderCountry,
    Country,
    MainFlag,
    HistoricalFlagPicture,
    DownloadablePictureFilePreview,
    DownloadablePictureFile,
)
from app.utils.pictures_utils import convert_and_compress_image, get_file_to_bytesio
# from app.flags.services import get_img_from_cdn
from app.utils.ru_slugify import custom_slugify

from .tasks import get_img_from_cdn_task  # get_flag_img_task,

# from django.core.files import File

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=DownloadablePictureFilePreview)
def if_image_updated(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = DownloadablePictureFilePreview.objects.get(pk=instance.pk)
        except DownloadablePictureFilePreview.DoesNotExist:
            return
        if old_image.image and instance.image and old_image.image.url != instance.image.url:
            path, file_name = os.path.split(old_image.webp.path)
            try:
                shutil.rmtree(path)
            except Exception:
                return
            old_image.image.delete(save=False)


@receiver(pre_save, sender=DownloadablePictureFilePreview)
def download_and_save_image(sender, instance, **kwargs):
    # if instance.url and not instance.svg:
    #     file = get_file_to_bytesio(url=instance.url)
    #     if file.ext == ".svg" and not instance.svg:
    #         instance.svg = File(file, f"{file.name}{file.ext}")

    if instance.url and not instance.image:
        try:
            file = get_file_to_bytesio(url=instance.url)
            instance.image = convert_and_compress_image(file=file, longest_side=1200)
            file.truncate()
            file.seek(0)
        except Exception as e:
            raise ValidationError({"url": f"Some problem: {e}"})


@receiver(post_save, sender=DownloadablePictureFilePreview)
def convert_svg(sender, instance, **kwargs):
    if instance.svg and not instance.image:
        file = convert_and_compress_image(get_file_to_bytesio(local_file=instance.svg))
        instance.image = file
        instance.save()


@receiver(post_delete, sender=DownloadablePictureFilePreview)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        try:
            path, file_name = os.path.split(instance.webp.path)
            shutil.rmtree(path)
        except Exception:
            return
        instance.image.delete(False)
        get_cache().clear()  # Actualy doesn't work
    if instance.svg:
        instance.svg.delete(False)


@receiver(post_delete, sender=DownloadablePictureFile)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(pre_save, sender=HistoricalFlagPicture)
def download_and_save_historical_image(sender, instance, **kwargs):
    if instance.url and not instance.image:
        try:
            file = get_file_to_bytesio(url=instance.url)
            instance.image = convert_and_compress_image(file=file, longest_side=1200)
            file.truncate()
            file.seek(0)
        except Exception as e:
            raise ValidationError({"url": f"Some problem: {e}"})


@receiver(post_save, sender=HistoricalFlagPicture)
def convert_historical_svg(sender, instance, **kwargs):
    if instance.svg and not instance.image:
        file = convert_and_compress_image(get_file_to_bytesio(local_file=instance.svg))
        instance.image = file
        instance.save()


@receiver(post_delete, sender=HistoricalFlagPicture)
def delete_historical_image(sender, instance, **kwargs):
    if instance.image:
        try:
            path, file_name = os.path.split(instance.webp.path)
            shutil.rmtree(path)
        except Exception:
            return
        instance.image.delete(False)
        get_cache().clear()  # Actualy doesn't work
    if instance.svg:
        instance.svg.delete(False)


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
def download_construction_image(sender, instance, **kwargs):
    if instance.construction_url and not instance.construction_image:
        try:
            file = get_file_to_bytesio(url=instance.construction_url)
            instance.construction_image = convert_and_compress_image(file=file, longest_side=1200)
            file.truncate()
            file.seek(0)
        except Exception as e:
            raise ValidationError({"construction_url": f"Some problem with cairosvg convert: {e}"})

    if instance.pk:
        try:
            old = MainFlag.objects.get(pk=instance.pk)
        except MainFlag.DoesNotExist:
            return
        if (
            old.construction_image
            and instance.construction_image
            and old.construction_image.url != instance.construction_image.url
        ):
            path, file_name = os.path.split(old.construction_webp.path)
            try:
                shutil.rmtree(path)
            except Exception:
                return
            old.construction_image.delete(save=False)


@receiver(pre_save, sender=MainFlag)
def befor_mainflag_save(sender, instance, **kwargs):
    # if instance.dl_imgs:
    #     result = get_flag_img_task.delay(instance.country.iso_code_a2)
    #     task_id = result.task_id  # noqa F841
    #     instance.dl_imgs = False
    if instance.dl_imgs:
        result = get_img_from_cdn_task.delay(instance.id, instance.country.iso_code_a2)
        task_id = result.task_id
        instance.dl_imgs = False


@receiver(post_save, sender=MainFlag)
def after_create_or_update_flag(sender, instance, **kwargs):
    if kwargs["created"]:
        # country = Country.objects.get(name=instance.country)
        # result = get_flag_img_task.delay(country.iso_code_a2)
        # task_id = result.task_id  # noqa F841
        result = get_img_from_cdn_task.delay(instance.id, instance.country.iso_code_a2)
        task_id = result.task_id
        instance.dl_imgs = False

    # if kwargs["created"]:
    #     get_img_from_cdn(instance.id, instance.country.iso_code_a2)

    # if instance.construction_image and not instance.construction_image_url and not instance.construction_webp:
    #     main, webp = convert(instance.construction_image.path, resize=300)
    #     instance.construction_image = f"construction/{main}"
    #     instance.construction_webp = f"construction/{webp}"
    #     instance.save()


@receiver(post_save, sender=Country)
def create_country_flag(sender, instance, **kwargs):
    if kwargs["created"]:
        # flag, _ = MainFlag.objects.get_or_create(country=instance)

        if instance.ru_name_rod:

            slug = custom_slugify(f"Флаг {instance.ru_name_rod}")
        else:
            slug = custom_slugify(f"Флаг {instance.name}")
        # if instance.en_short_form:
        #     slug = slugify(f'flag of {instance.en_short_form}')
        # else:
        #     slug = slugify(f'{instance.iso_code_a2} flag')

        try:
            flag = MainFlag.objects.get(country=instance)
        except MainFlag.DoesNotExist:
            flag = MainFlag(
                country=instance,
                title=f"Флаг {instance.ru_name_rod}",
                slug=slug,
            )
            flag.save()


'''
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
def delete_image2(sender, instance, **kwargs):
    if instance.image:
        remove_historical_flag_img(instance.image.path)
    if instance.webp:
        remove_historical_flag_img(instance.webp.path)


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
'''
