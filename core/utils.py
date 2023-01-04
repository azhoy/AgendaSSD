from .models import ContactRequest


def get_friend_request_or_false(sender, receiver):
    try:
        return ContactRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except ContactRequest.DoesNotExist:
        return False
