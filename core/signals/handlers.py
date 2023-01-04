from django.conf import settings
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from core.models import User, ContactList


# This method will create a contact list object automatically at users creation
@receiver(post_save, sender=User)
def create_contact_list_for_new_user(sender, **kwargs):
    if kwargs['created']:
        ContactList.objects.create(user=kwargs['instance'])
