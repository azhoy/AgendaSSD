import uuid

from rest_framework import serializers
from core.models import User, Event, Invitation, ContactList, ContactRequest

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer)


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
            'public_key',
            'protected_private_key',
            'protected_symmetric_key',
        ]


# Sub serializer for the 'event_invited_to' field in the User
class EventInvitedToSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='get_event_id')
    title = serializers.ReadOnlyField(source='get_event_title')
    start_date = serializers.ReadOnlyField(source='get_event_start_date')

    class Meta:
        model = Invitation
        fields = ['event_id', 'title', 'start_date']


# Sub serializer for the 'event_created' field in the User
class EventCreatedSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Event
        fields = ['event_id', 'title', 'start_date']


# 2. User profile serializer
class UserSerializer(BaseUserSerializer):
    # username = serializers.ReadOnlyField()
    event_created = EventCreatedSerializer(many=True)
    event_invited_to = EventInvitedToSerializer(many=True)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'email',
            'username',
            'public_key',
            'protected_private_key',
            'protected_symmetric_key',
            'event_created',
            'event_invited_to',
        ]


# Only display username of the other users
class OtherUserSerializer(BaseUserSerializer):
    username = serializers.ReadOnlyField()

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'username'
        ]


# For every other request, hide just in case
class HideUserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
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
        payload = {}
        # Getting the sender of the friend request user object
        active_member = User.objects.get(id=self.context['user_id'])
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
                            raise Exception("You already sent a contact request.")
                    # If none are active, then create a new friend request
                    contact_request = ContactRequest(sender=active_member, receiver=receiver)
                    contact_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = f"{e}"
            except ContactRequest.DoesNotExist:
                # This user has never sent a friend request => Create one
                contact_request = ContactRequest(sender=active_member, receiver=receiver)
                contact_request.save()
                payload['response'] = "Friend request sent."
        except Exception as e:
            print(e)


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
        payload = {}
        # Getting the receiver of the friend request user object == active user
        active_user = User.objects.get(id=self.context['user_id'])
        # Getting the receiver of the friend request user object
        try:
            sender = User.objects.get(username=self.context['username_to_accept'][0])
            try:
                # Get any friend request active and not active between these 2
                contact_request = ContactRequest.objects.get(sender=sender, receiver=active_user, is_active=True)
                contact_request.accept()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

class DeclineContactSerializer(serializers.Serializer):
    username_to_decline = serializers.CharField()

    def save(self, **kwargs):
        payload = {}
        # Getting the receiver of the friend request user object == active user
        active_user = User.objects.get(id=self.context['user_id'])
        # Getting the receiver of the friend request user object
        try:
            sender = User.objects.get(username=self.context['username_to_decline'][0])
            try:
                # Get any friend request active and not active between these 2
                contact_request = ContactRequest.objects.get(sender=sender, receiver=active_user, is_active=True)
                contact_request.decline()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


class DeleteContactSerializer(serializers.Serializer):
    username_to_delete = serializers.CharField()

    def save(self, **kwargs):
        payload = {}
        # Getting the sender of the friend request user object
        active_member = User.objects.get(id=self.context['user_id'])
        # Getting the receiver of the friend request user object
        try:
            removee = User.objects.get(username=self.context['username_to_delete'][0])
            try:
                # Get any friend request active and not active between these 2
                contact_list = ContactList.objects.get(user=active_member)
                contact_list.unfriend(removee=removee)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


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
    event_id = serializers.CharField(source='event.id', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_start_date = serializers.CharField(source='event.start_date', read_only=True)
    member_invited = serializers.CharField(source='member_invited.username', read_only=True)
    member_protected_event_key = serializers.CharField(source='invited_member_protected_event_key', read_only=True)
    acceptedStatus = serializers.CharField(read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'invitation_id',
            'event_id',
            'event_title',
            'event_start_date',
            'member_invited',
            'member_protected_event_key',
            'acceptedStatus'
        ]


class UpdateInvitationsSerializer(serializers.ModelSerializer):
    invitation_id = serializers.UUIDField(source='id', read_only=True)
    event_id = serializers.UUIDField(source='event.id', read_only=True)
    event_title = serializers.UUIDField(source='event.title', read_only=True)
    event_start_date = serializers.UUIDField(source='event.start_date', read_only=True)
    member_invited = serializers.UUIDField(source='member_invited.username', read_only=True)
    member_protected_event_key = serializers.CharField(source='invited_member_protected_event_key', read_only=True)

    class Meta:
        model = Invitation
        fields = [
            'invitation_id',
            'event_id',
            'event_title',
            'event_start_date',
            'member_invited',
            'member_protected_event_key',
            'acceptedStatus'
        ]


class AddInvitationsSerializer(serializers.Serializer):
    username_to_invite = serializers.CharField()

    def save(self, **kwargs):
        # Getting the creator user object
        active_member = User.objects.get(id=self.context['user_id'])
        try:
            # Getting the event object to invite to
            event = Event.objects.prefetch_related('creator').get(id=self.context['event_id'])
            # If the users to invite exists => if the username input is correct
            try:
                member_invited = User.objects.get(username=self.context['username_to_invite'][0])

                # If the creator contact list exists
                try:
                    creator_contact_list = ContactList.objects.get(user_id=self.context['user_id'])
                except ContactList.DoesNotExist:
                    creator_contact_list = ContactList(user_id=self.context['user_id'])
                    creator_contact_list.save()


                """
                # Accessing all the contacts of the creator
                creator_contacts = creator_contact_list.contacts.all()

                # If the active member is the creator of the event
                if event.creator.id == active_member.id:
                    # If the member invited is in the contact list (change with username if proble
                    if member_invited.id in creator_contacts:
                        Invitation.objects.create(
                            event=event,
                            member_invited=member_invited,
                        )
                """
                # If the active user is the creator of the event
                if event.creator.id == active_member.id:
                    # If the invited member is in the contact list of the creator of the event
                    if creator_contact_list.is_mutual_contact(member_invited):
                        Invitation.objects.create(
                            event=event,
                            member_invited=member_invited,
                        )
            except Exception as e:
                print(e)
                print('The username doesnt exist')
        except Exception as e:
            print(e)
            print('This event doesnt exist')
        # else:
        # print('this user doesnt exist')


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
    invited = InvitationsSerializer(many=True, read_only=True)

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
            'invited'  # ???
        ]


class UpdateEventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    protected_event_key = serializers.CharField(read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    invited = InvitationsSerializer(many=True, read_only=True)

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
            'invited'
        ]


class AddEventSerializer(serializers.Serializer):
    protected_event_key = serializers.CharField()
    title = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField(allow_blank=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    location = serializers.CharField(allow_blank=True, allow_null=True)

    def save(self, **kwargs):
        # Get the member profile

        member = User.objects.get(id=self.context['user_id'])
        # Save the event
        Event.objects.create(
            creator=member,
            protected_event_key=self.context['protected_event_key'][0],
            title=self.context['title'][0],
            start_date=self.context['start_date'][0],
            end_date=self.context['end_date'][0],
            description=self.context['description'][0],
            location=self.context['location'][0],
        )


class HideEventsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
        ]
