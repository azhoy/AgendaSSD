from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.core.models import User, ContactList


# This method will create a contact list object automatically at users creation
@receiver(post_save, sender=User)
def create_contact_list_for_new_user(sender, **kwargs):
    if kwargs['created']:
        ContactList.objects.create(user=kwargs['instance'])
