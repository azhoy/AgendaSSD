from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Event, Member, EventParticipant
from .serializers import (
    EventSerializer, UpdateEventSerializer, AddEventSerializer, HideEventsSerializers,
    MemberSerializer, UpdateMemberSerializer, OtherMemberSerializer, HideMemberSerializer,
    InvitationsSerializer, UpdateInvitationsSerializer, AddInvitationsSerializer, HideInvitationsSerializer)


class MemberViewSet(UpdateModelMixin, GenericViewSet):
    queryset = Member.objects.all()

    # All actions in this class are not available to unauthenticated users
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "me":
            # Serializer for "my profile page"
            return MemberSerializer
        elif self.action == "update_contacts":
            # Serializer to update contact field
            return UpdateMemberSerializer
        elif self.action == "everybody":
            # Serializer to update contact field
            return OtherMemberSerializer
        else:
            # Serializer to see other member profile
            return HideMemberSerializer

    # detail=False: Action available on the list view
    # detail=True: Action available on the detail view
    @action(detail=False, methods=['GET'])
    def me(self, request):
        # Get the current profile
        # Create it and link it to the current user if it doesn't exist
        member = Member.objects.get(user_id=request.user.id)
        # Retrieve member profile information
        if request.method == 'GET':
            serializer = MemberSerializer(member)
            # print(f"serializer.data: {serializer.data}")
            return Response(serializer.data)

    # Usernames of others member exposed
    @action(detail=False, methods=['GET'])
    def everybody(self, request):
        # Get the current profile
        # Create it and link it to the current user if it doesn't exist
        members = Member.objects.all()
        # Retrieve all members profile information
        if request.method == 'GET':
            member_list = []
            for member in members:
                serializer = OtherMemberSerializer(member)
                # print(f"event serializer.data: {serializer.data}")
                member_list.append(serializer.data)
            return Response(member_list)

    @action(detail=False, methods=['PUT'])
    def update_contacts(self, request):
        # Get the current profile
        # Create it and link it to the current user if it doesn't exist
        member = Member.objects.get(user_id=request.user.id)
        # Update member profile information (contacts field)
        if request.method == 'PUT':
            serializer = UpdateMemberSerializer(member, data=request.data)
            # print(f"request.data: {request.data}")
            # print(f"request.user: {request.user.id}")
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #  print(f"serializer.data: {serializer.data}")
            return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}


class InvitationViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateInvitationsSerializer
        elif self.request.method == 'GET':
            return InvitationsSerializer
        elif self.request.method == 'POST':
            return AddInvitationsSerializer
        return HideInvitationsSerializer

    def get_queryset(self):
        member = Member.objects.get(user_id=self.request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=self.kwargs['event_pk'])
        # A member can see the invitations of an event he created
        if member.id == event.creator.id:
            return EventParticipant.objects.filter(event_id=self.kwargs['event_pk'])
        # A member can see the invitations of an event he is invited to
        for invitation in event.participants.all():
            if member.id == invitation.invited_member.id:
                return EventParticipant.objects.filter(event_id=self.kwargs['event_pk'])

    def update(self, request, *args, **kwargs):
        member = Member.objects.get(user_id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['event_pk'])
        if getattr(event, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            event._prefetched_objects_cache = {}

        for invitation in event.participants.all():
            # Only the invited member can modify the status of its invitation
            if member.id == invitation.invited_member.id:
                serializer = self.get_serializer(invitation, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Forbidden. NOT your invitation'})

    def get_serializer_context(self):
        return {
            'request': self.request,
            'event_id': self.kwargs['event_pk'],
            'user_id': self.request.user.id,
            'invited_member': self.request.POST.getlist('invited_member'),
        }


class EventViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Event.objects.prefetch_related('creator').all()
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Event.objects.prefetch_related('creator').all()

        member_id = Member.objects.only('id').get(user_id=user.id)
        return Event.objects.prefetch_related('creator').filter(creator_id=member_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'title': self.request.POST.getlist('title'),
            'start_date': self.request.POST.getlist('start_date'),
            'end_date': self.request.POST.getlist('end_date'),
            'description': self.request.POST.getlist('description'),
            'location': self.request.POST.getlist('location'),
        }

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateEventSerializer
        elif self.request.method == 'POST':
            return AddEventSerializer
        else:
            # Serializer to hide events details in the endpoint for non-related user
            return EventSerializer

    @action(detail=False, methods=['GET'])
    def my_invitations(self, request):
        member = Member.objects.get(user_id=request.user.id)
        # Get a queryset object all events to which the current active user was invited to
        events = Event.objects.prefetch_related('creator').filter(participants__invited_member=member.id)
        event_list = []
        for event in events:
            serializer = EventSerializer(event)
            # print(f"event serializer.data: {serializer.data}")
            event_list.append(serializer.data)
        return Response(event_list)

    def update(self, request, *args, **kwargs):
        member = Member.objects.get(user_id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['pk'])
        if getattr(event, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            event._prefetched_objects_cache = {}

        # Only the creator of the event can update this event
        if member.id == event.creator.id:
            serializer = self.get_serializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Forbidden. NOT your event'})

    # Overriding the delete method
    def destroy(self, request, *args, **kwargs):
        member = Member.objects.get(user_id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['pk'])
        # Only the creator of an event can delete this event
        if member.id == event.creator.id:
            event.delete()
            return Response({'message': 'Event deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Forbidden. NOT your event'})
