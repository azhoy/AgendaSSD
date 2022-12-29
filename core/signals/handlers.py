from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Member


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_for_new_user(sender, **kwargs):
    # If a new user is created
    if kwargs['created']:
        # Create a member
        Member.objects.create(user=kwargs['instance'])

