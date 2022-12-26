from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .filters import EventFilter, MemberFilter
from .models import Event, Member, EventParticipant
from .serializers import (
    EventSerializer, AddEventSerializer,
    MemberSerializer, AddMemberSerializer, UpdateMemberSerializer,
    EventParticipantsSerializer, UpdateEventParticipantsSerializer)


# All the methods except DestroyModelMixin => Cannot delete Member
class MemberViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Member.objects.all()

    # permission_classes = [IsAuthenticated ]# All actions in this class are not available to unauthenticated users
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddMemberSerializer
        elif self.request.method == 'PUT':
            return UpdateMemberSerializer
        return MemberSerializer

    # NOTE: Search through custom_id field for Member instances
    # http://127.0.0.1:8100/agenda/member/?search=<custom_id>/
    filter_backends = [SearchFilter]
    filterset_class = MemberFilter
    search_fields = ['id']

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (member, created) = Member.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = MemberSerializer(member, data=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class EventParticipantsViewSet(ModelViewSet):
    """Get all participation request with the GET methods
    Create a participation request with the POST methods
    Change the status of a request with the PUT or PATCH methods (id in the endpoints)
    """
    # permission_classes = [IsAuthenticated ]# All actions in this class are not available to unauthenticated users

    http_method_names = ['get', 'post', 'put', 'patch']

    # Only allow the modification of AcceptedStatus Fields
    # => All other fields are constant a user can refuse or accept an invitation
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateEventParticipantsSerializer
        return EventParticipantsSerializer

    def get_queryset(self):
        return EventParticipant.objects.filter(event_id=self.kwargs['event_pk'])


class EventViewSet(ModelViewSet):
    """Get all core (Agenda) with the GET methods
    Add an event to the agenda with the POST method
    Delete an event with the DELETE methods (id in the endpoints)
    Modify an event with the PUT method (id in the endpoints)
    Modify a single field of an event with the PATCH method (id in the endpoints)"""

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    queryset = Event.objects.prefetch_related('creator').all()

    # permission_classes = [IsAuthenticated ]# All actions in this class are not available to unauthenticated users

    # Allow to add 'creator' field at event creation but not at event modification
    # => We set creator for an event but cannot modify it
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddEventSerializer
        return EventSerializer

    # NOTE: Filter search through 'creator' => Get all core created by a member <custom_id>
    # http://127.0.0.1:8100/agenda/events/?creator=<custom_id>/
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_context(self):
        return {'request': self.request}
