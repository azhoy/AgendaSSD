from rest_framework import serializers
from core.models import Member, Event, EventParticipant
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


# Djoser auth model
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # Override
        fields = [
            'id',
            'username',
            'password'
        ]


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'id',
            'user_id',  # Not
            'contacts',
            'created_events',
            'invited_events'
        ]


# TODO: Manage Django Auth User Object
class AddMemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField()  # TODO: DELETE in prod

    class Meta:
        model = Member
        fields = [
            'id',
            'user_id',  # TODO: DELETE in PROD
            'contacts',
        ]


# Only allow contacts modification for a member
class UpdateMemberSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Member
        fields = [
            'id',
            'contacts',
        ]


class EventParticipantsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'id',
            'event',
            'invited_member',
            'acceptedStatus'
        ]


class UpdateEventParticipantsSerializer(serializers.ModelSerializer):
    invited_member = serializers.UUIDField(read_only=True)
    event = serializers.UUIDField(read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = EventParticipant
        fields = [
            'id',
            'event',
            'invited_member',
            'acceptedStatus'
        ]


class EventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    creator = serializers.CharField(read_only=True)
    participants = EventParticipantsSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'creator',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
            'participants'
        ]


class AddEventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    participants = EventParticipantsSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'creator',
            'title',
            'start_date',
            'end_date',
            'description',
            'location',
            'participants'
        ]
