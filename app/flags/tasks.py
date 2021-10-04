from celery import shared_task

# from app.utils.flag_image import get_flag_img
from app.flags.services import get_img_from_cdn


# @shared_task(bind=True, soft_time_limit=100, time_limit=120)
# def get_flag_img_task(self, iso2):
#     get_flag_img(iso2)


@shared_task(bind=True, soft_time_limit=100, time_limit=120)
def get_img_from_cdn_task(self, flag_id, iso2):
    get_img_from_cdn(flag_id, iso2)
