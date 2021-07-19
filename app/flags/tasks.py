from celery import shared_task

from app.utils.flag_image import get_flag_img


@shared_task(bind=True, soft_time_limit=100, time_limit=120)
def get_flag_img_task(self, iso2):
    get_flag_img(iso2)
