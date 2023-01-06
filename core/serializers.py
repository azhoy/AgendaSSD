import logging

from rest_framework import serializers
from core.models import User, Event, Invitation, ContactList, ContactRequest
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer)
from django.core.mail import EmailMessage
from django.conf import settings

from django.db import IntegrityError, transaction



# ####################################################################################################@
# Logger configuration
# ####################################################################################################@

class RecordCounter:
    _instance = None
    _count = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def count(self):
        self._count += 1
        return self._count


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.record_number = RecordCounter().count()
        return True


logging.basicConfig(level=logging.WARNING,
                    #format='%(record_number)s [%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(settings.LOGS_FILE),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

# ####################################################################################################@
# User Serializers
# ####################################################################################################@

# 1. User creation serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'email',
            'username',  # If mandatory => Auto generate on client side
            'password',
            're_password',
            'public_key',
            'protected_private_key',
            'protected_symmetric_key',
        ]


# 2. User profile serializer
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'username',
            'public_key',
            'protected_private_key',
            'protected_symmetric_key',
        ]


# For every other request, Use a default serializer that doesn't show any information
class HideUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
        ]


# ####################################################################################################@
# Contact Serializers
# ####################################################################################################@

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = [
            'contacts'
        ]


class AddContactRequestSerializer(serializers.Serializer):
    username_to_add = serializers.CharField()

    def save(self, **kwargs):
        try:
            # Getting the sender of the friend request user object
            active_member = User.objects.get(username=self.context['username'])
            # Getting the receiver of the friend request user object
            try:
                receiver = User.objects.get(username=self.context['username_to_add'][0])
                try:
                    # Get any friend request active and not active between these 2
                    contact_request = ContactRequest.objects.filter(sender=active_member, receiver=receiver)
                    # Find if any contact request is active
                    try:
                        for request in contact_request:
                            if request.is_active:
                                print("You already sent a contact request.")
                        # If none are active, then create a new friend request
                        contact_request = ContactRequest(sender=active_member, receiver=receiver)
                        contact_request.save()
                        email = EmailMessage(
                            'New contact request !',
                            f'{active_member.username} just sent you a contact request !',
                            settings.EMAIL_HOST_USER,
                            [f'{receiver.email}']
                        )
                        email.send()
                    except Exception as e:
                        print(e)
                except ContactRequest.DoesNotExist:
                    # This user has never sent a friend request => Create one
                    contact_request = ContactRequest(sender=active_member, receiver=receiver)
                    contact_request.save()
            except User.DoesNotExist:
                logger.info(f"{active_member.username} tried to contact request a user that does not exist")
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


# ####################################################################################################@
# Contact Request Serializers
# ####################################################################################################@

class ContactRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = ContactRequest
        fields = [
            'sender',
            'receiver',
            'is_active'
        ]


class AcceptContactSerializer(serializers.Serializer):
    username_to_accept = serializers.CharField()

    def save(self, **kwargs):
        try:
            # Getting the receiver of the friend request user object == active user
            active_user = User.objects.get(username=self.context['username'])
            # Getting the receiver of the friend request user object
            try:
                sender = User.objects.get(username=self.context['username_to_accept'][0])
                try:
                    # Get any friend request active and not active between these 2
                    contact_request = ContactRequest.objects.get(sender=sender, receiver=active_user, is_active=True)
                    contact_request.accept()
                    # Mail n°1
                    email_1 = EmailMessage(
                        'New contact !',
                        f'{sender.username} is now in your contact list',
                        settings.EMAIL_HOST_USER,
                        [f'{active_user.email}']
                    )
                    email_1.send()

                    # Mail n°2
                    email_2 = EmailMessage(
                        'New contact !',
                        f'{active_user.username} is now in your contact list',
                        settings.EMAIL_HOST_USER,
                        [f'{sender.email}']
                    )
                    email_2.send()

                except ContactRequest.DoesNotExist:
                    logger.info(f"{active_user.username} tried to accept a user that did not invite him")
            except User.DoesNotExist:
                logger.info(f"{active_user.username} tried to accept a user that does not exist")
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


class DeclineContactSerializer(serializers.Serializer):
    username_to_decline = serializers.CharField()

    def save(self, **kwargs):
        try:
            # Getting the receiver of the friend request user object == active user
            active_user = User.objects.get(username=self.context['username'])
            # Getting the receiver of the friend request user object
            try:
                sender = User.objects.get(username=self.context['username_to_decline'][0])
                try:
                    # Get any friend request active and not active between these 2
                    contact_request = ContactRequest.objects.get(sender=sender, receiver=active_user, is_active=True)
                    contact_request.decline()
                except ContactRequest.DoesNotExist:
                    logger.info(f"{active_user.username} tried to decline a user that did not invite him")
            except User.DoesNotExist:
                logger.info(f"{active_user.username} tried to decline a user that does not exist")
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


class DeleteContactSerializer(serializers.Serializer):
    username_to_delete = serializers.CharField()

    def save(self, **kwargs):
        try:
            # Getting the sender of the friend request user object
            active_member = User.objects.get(username=self.context['username'])
            # Getting the receiver of the friend request user object
            try:
                removee = User.objects.get(username=self.context['username_to_delete'][0])
                try:
                    # Get any friend request active and not active between these 2
                    contact_list = ContactList.objects.get(user=active_member)
                    contact_list.unfriend(removee=removee)
                except ContactList.DoesNotExist:
                    logger.warning(
                        f"{active_member.username} does not have a contact list. User not created normally !")
            except User.DoesNotExist:
                logger.info(f"{active_member.username} tried to delete a user that does not exist")
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


class HideContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = [
        ]


# ####################################################################################################@
# Invitations Serializers
# ####################################################################################################@

class InvitationsSerializer(serializers.ModelSerializer):
    invitation_id = serializers.UUIDField(source='id', read_only=True)
    user_invited = serializers.CharField(source='user_invited.username', read_only=True)
    protected_event_key = serializers.CharField(read_only=True)
    protected_event_id = serializers.CharField(read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'invitation_id',
            'user_invited',
            'protected_event_key',
            'protected_event_id',
        ]


class AddInvitationsSerializer(serializers.Serializer):
    username_to_invite = serializers.CharField()
    # The id of the event ciphered with the key generated for the invitation from the user public_key
    # Only the invited user can decipher it with is private_key and know to which event he was invited to
    protected_event_id = serializers.CharField()

    # Event key encrypted with the user invited public key
    protected_event_key = serializers.CharField()

    # Field with the new participants list
    protected_participants_list = serializers.CharField()

    def save(self, **kwargs):
        # Getting the creator user object
        try:
            active_member = User.objects.get(username=self.context['username'])
            try:
                # Getting the event object to invite to
                # The id of the event is taken from the URL on the client side
                # The server can't see its value
                event = Event.objects.prefetch_related('creator').get(id=self.context['event_id'])
                # If the users to invite exists => if the username input is correct
                try:
                    user_invited = User.objects.get(username=self.context['username_to_invite'][0])

                    # If the creator contact list exists
                    try:
                        creator_contact_list = ContactList.objects.get(user__username=self.context['username'])
                    except ContactList.DoesNotExist:
                        creator_contact_list = ContactList(user__username=self.context['username'])
                        creator_contact_list.save()

                    # If the active user is the creator of the event
                    if event.creator.id == active_member.id:
                        # If the invited member is in the contact list of the creator of the event
                        if creator_contact_list.is_mutual_contact(user_invited):
                            # Create an invitation for the user that enables him to read the ciphered event detail
                            Invitation.objects.create(
                                user_invited=user_invited,
                                protected_event_key=self.context['protected_event_key'][0],
                                protected_event_id=self.context['protected_event_id'][0]
                            )

                            # Updating the list of participants
                            event.update_participants(self.context['protected_participants_list'][0])
                        else:
                            logger.info(
                                f"{active_member.username} tried to invite {user_invited.username} but this user is not in its contact list")
                    else:
                        logger.warning(
                            f"{active_member.username} tried to invite {user_invited.username} to {event.creator.username} event")
                except User.DoesNotExist:
                    logger.info(f'{active_member.username} tried to invite a user that doesnt exist to an event')
            except Exception as e:
                logger.warning(f'{active_member.username} tried to access an invalid event via the URL')
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


class HideInvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
        ]


# ####################################################################################################@
# Events Serializers
# ####################################################################################################@


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    protected_event_key = serializers.CharField(read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'protected_event_key',
            'creator_username',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
            'participants'
        ]


class MyCreatedEventsSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'title',
            'start_date',
            'end_date',
        ]


class UpdateEventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    protected_event_key = serializers.CharField(read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    title = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'protected_event_key',
            'creator_username',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
        ]


class AddEventSerializer(serializers.Serializer):
    protected_event_key = serializers.CharField()
    title = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField(allow_blank=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    location = serializers.CharField(allow_blank=True, allow_null=True)


    def save(self, **kwargs):
        try:
            # Get the user profile
            active_user = User.objects.get(username=self.context['username'])
            # Save the event
            Event.objects.create(
                creator=active_user,
                protected_event_key=self.context['protected_event_key'],
                title=self.context['title'],
                start_date=self.context['start_date'],
                end_date=self.context['end_date'],
                description=self.context['description'],
                location=self.context['location'],
            )
            logger.info(f"{active_user.username} created an event")
        except User.DoesNotExist:
            logger.critical(
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB"
            )
            # Mail to admin
            alert_email = EmailMessage(
                'Critical alert - Django server',
                f"The user {self.context['username']} is authenticated from the JWT request but does not exist in the DB",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()


class HideEventsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
        ]
