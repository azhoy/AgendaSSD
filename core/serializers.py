import uuid

from rest_framework import serializers
from core.models import Member, Event, EventParticipant
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


# ====
# Profile and Member Serializers
# ====

# Authentication user model serializer
# /auth/users/me/ (GET)
# /auth/users/ (PUT)
# /auth/jwt/create/ (POST)
class UserCreateSerializer(BaseUserCreateSerializer):
    # username and password are the only field mandatory for a user instance
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id',
            'username',
            'password'
        ]


# Sub serializer for the 'invited_events'field in the MemberSerializer
class InvitedEventsSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='get_event_id')
    title = serializers.ReadOnlyField(source='get_event_title')
    start_date = serializers.ReadOnlyField(source='get_event_start_date')

    class Meta:
        model = EventParticipant
        fields = ['event_id', 'title', 'start_date']


# Sub serializer for the 'created_events'field in the MemberSerializer
class CreatedEventsSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Event
        fields = ['event_id', 'title', 'start_date']


# Display information of the connected member
# /agenda/member/me/ (GET)
class MemberSerializer(serializers.ModelSerializer):
    created_events = CreatedEventsSerializer(many=True)
    invited_events = InvitedEventsSerializer(many=True)
    username = serializers.ReadOnlyField(source='get_username')
    contacts = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'username',
            'contacts',
            'created_events',
            'invited_events'
        ]


# Only allow contacts modification for a member connected
# /agenda/member/update_contacts/ (PUT)
class UpdateMemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='get_username')

    class Meta:
        model = Member
        fields = [
            'username',
            'contacts',
        ]


# Display information of the other member
# /agenda/member/ (GET)
class OtherMemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='get_username')

    class Meta:
        model = Member
        fields = [
            # 'id',
            'username'
        ]


# ====
# Invitations serializers
# ====

class InvitationsSerializer(serializers.ModelSerializer):
    invitation_id = serializers.UUIDField(source='id', read_only=True)
    event_id = serializers.UUIDField(source='event.id', read_only=True)
    event_title = serializers.UUIDField(source='event.title', read_only=True)
    event_start_date = serializers.UUIDField(source='event.start_date', read_only=True)
    member_invited = serializers.UUIDField(source='invited_member.get_username', read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'invitation_id',
            'event_id',
            'event_title',
            'event_start_date',
            'member_invited',
        ]


class UpdateInvitationsSerializer(serializers.ModelSerializer):
    member_invited = serializers.UUIDField(source='invited_member.get_username', read_only=True)
    event_id = serializers.UUIDField(source='event.id', read_only=True)
    event_title = serializers.UUIDField(source='event.title', read_only=True)
    event_start_date = serializers.UUIDField(source='event.start_date', read_only=True)
    invitation_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'invitation_id',
            'event_id',
            'event_title',
            'event_start_date',
            'member_invited',
            'acceptedStatus'
        ]


class AddInvitationsSerializer(serializers.Serializer):
    invited_member = serializers.UUIDField()

    def save(self, **kwargs):
        event = Event.objects.prefetch_related('creator').get(id=self.context['event_id'])
        invited_member = Member.objects.get(id=self.context['invited_member'][0])
        active_member = Member.objects.get(user_id=self.context['user_id'])
        # If the active member is the creator of the event
        if event.creator.id == active_member.id:
            # TODO 1: Add a contdition to check if the member exist
            # TODO 2: Add another condition with the contact list
            # Save the event
            invitation = EventParticipant.objects.create(
                event=event,
                invited_member=invited_member,
            )



# ====
# Events serializers
# ====


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    creator_username = serializers.CharField(source='creator.get_username', read_only=True)
    participants = InvitationsSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'creator_username',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
            'participants'
        ]


class UpdateEventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    creator_username = serializers.CharField(source='creator.get_username', read_only=True)
    participants = InvitationsSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'creator_username',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
            'participants'
        ]


class AddEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField(allow_blank=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    location = serializers.CharField(allow_blank=True, allow_null=True)

    def save(self, **kwargs):
        # Get the member profile

        member = Member.objects.get(user_id=self.context['user_id'])
        # Save the event
        Event.objects.create(
            creator=member,
            title=self.context['title'][0],
            start_date=self.context['start_date'][0],
            end_date=self.context['end_date'][0],
            description=self.context['description'][0],
            location=self.context['location'][0],
        )

    # ====


# Hidden serializers
# ====

class HideEventsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
        ]


class HideMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
        ]


class HideInvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = [
        ]
