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
        fields = ['event_id',  'title', 'start_date']


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

class EventParticipantsSerializer(serializers.ModelSerializer):
    invitation_id = serializers.UUIDField(source='id', read_only=True)
    event_id = serializers.UUIDField(source='event.id')
    member_invited = serializers.UUIDField(source='invited_member.get_username')

    class Meta:
        model = EventParticipant
        fields = [
            'invitation_id',
            'event_id',
            'member_invited',
        ]


class UpdateEventParticipantsSerializer(serializers.ModelSerializer):
    member_invited = serializers.UUIDField(source='invited_member.get_username', read_only=True)
    event_id = serializers.UUIDField(source='event', read_only=True)
    invitation_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'invitation_id',
            'event_id',
            'member_invited',
            'acceptedStatus'
        ]


# ====
# Events serializers
# ====


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)
    creator_username = serializers.CharField(source='creator.get_username', read_only=True)
    participants = EventParticipantsSerializer(many=True, read_only=True)

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
    participants = EventParticipantsSerializer(many=True, read_only=True)

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
class AddEventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'creator',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
        ]

    def create(self, validated_data):
        return Event.objects.create(**validated_data)


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



