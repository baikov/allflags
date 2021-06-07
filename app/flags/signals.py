from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import BorderCountry, Country


@receiver(post_save, sender=Country)
def test_country_postsave(sender, instance, **kwargs):
    print("Country Post_save")


@receiver(post_save, sender=BorderCountry)
def create_neighbour(sender, instance, **kwargs):
    print("Post_save")


@receiver(post_delete, sender=BorderCountry)
def delete_neighbour(sender, instance, **kwargs):
    print("Post_delete")


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
