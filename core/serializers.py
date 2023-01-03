import uuid

from rest_framework import serializers
from core.models import User, Event, Invitation

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer)


# ====
# User profile serializer
# ====

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


# 2. User profile serializer

# 2.1 Sub serializer for the 'event_invited_to' field in the User
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


# Sub serializer for the 'my_contacts' field in the User
class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['contact_id']


# Display information of the connected member
# /agenda/member/me/ (GET)

class UserSerializer(BaseUserSerializer):
    # username = serializers.ReadOnlyField()
    event_created = EventCreatedSerializer(many=True)
    event_invited_to = EventInvitedToSerializer(many=True)
    my_contacts = ContactListSerializer(many=True)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'email',
            'username',
            'public_key',
            'protected_private_key',
            'protected_symmetric_key',
            'event_created',
            'event_invited_to',
            'my_contacts'
        ]


# Display information of the other member
class OtherUserSerializer(BaseUserSerializer):
    username = serializers.ReadOnlyField()

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'username'
        ]


# /agenda/member/update_contacts/ (PUT)
class UpdateContactSerializer(BaseUserSerializer):
    username = serializers.ReadOnlyField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            'username',
            'protected_contact_list',
        ]


class HideUserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
        ]


# ====
# Invitations serializers
# ====

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
    member_invited = serializers.UUIDField()

    def save(self, **kwargs):
        event = Event.objects.prefetch_related('creator').get(id=self.context['event_id'])
        member_invited = User.objects.get(id=self.context['member_invited'][0])
        active_member = User.objects.get(id=self.context['user_id'])
        # If the active member is the creator of the event
        if event.creator.id == active_member.id:
            # TODO 1: Add a contdition to check if the member exist
            # TODO 2: Add another condition with the contact list
            # Save the event
            Invitation.objects.create(
                event=event,
                member_invited=member_invited,
            )


class HideInvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
        ]


# ====
# Events serializers
# ====


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

