from django.shortcuts import render
from djoser.views import UserViewSet
from djoser.conf import settings as djoser_settings
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Event, User, Invitation, ContactList, ContactRequest
from .serializers import (
    ContactSerializer, AddContactRequestSerializer, ContactRequestSerializer, HideContactSerializer,
    AcceptContactSerializer, DeclineContactSerializer, DeleteContactSerializer, HideUserSerializer, OtherUserSerializer,
    EventSerializer, UpdateEventSerializer, AddEventSerializer, HideEventsSerializers,
    InvitationsSerializer, UpdateInvitationsSerializer, AddInvitationsSerializer, HideInvitationsSerializer)


# ####################################################################################################@
# User Viewsets
# ####################################################################################################@


class CustomUserViewSet(UserViewSet):

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = djoser_settings.PERMISSIONS.user_create  # ["rest_framework.permissions.AllowAny"]
        elif self.action == "list":
            self.permission_classes = djoser_settings.PERMISSIONS.user_list  # ["djoser.permissions.CurrentUserOrAdmin"]
        elif self.action == "set_password":
            self.permission_classes = djoser_settings.PERMISSIONS.set_password  # ["djoser.permissions.CurrentUserOrAdmin"]
        elif self.action == "set_username":
            self.permission_classes = djoser_settings.PERMISSIONS.set_username  # ["djoser.permissions.CurrentUserOrAdmin"]
        return super().get_permissions()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
        }

    def get_serializer_class(self):
        if self.action == "create":
            if djoser_settings.USER_CREATE_PASSWORD_RETYPE:
                return djoser_settings.SERIALIZERS.user_create_password_retype
            return djoser_settings.SERIALIZERS.user_create  # core.serializers.UserCreateSerializer
        elif self.action == "set_password":
            if djoser_settings.SET_PASSWORD_RETYPE:
                return djoser_settings.SERIALIZERS.set_password_retype
            return djoser_settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if djoser_settings.SET_USERNAME_RETYPE:
                return djoser_settings.SERIALIZERS.set_username_retype
            return djoser_settings.SERIALIZERS.set_username
        elif self.action == "me":
            return djoser_settings.SERIALIZERS.current_user
        return HideUserSerializer

    # Override the '/users/me/' to prevent the modification of 'protected_symmetric_key' field by a user
    # The authenticated user can only retrieve its information
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

    """
    # List the usernames of all users
    @action(["get"], detail=False)
    def all_users(self, request, *args, **kwargs):
        all_users = User.objects.all()
        if request.method == "GET":
            username_list = []
            for username in all_users:
                serializer = OtherUserSerializer(username)
                username_list.append(serializer.data)
            return Response(username_list)
    """

    # Overriding all the unnecessary actions from the djoser package
    @action(["get"], detail=False)
    def activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


# ####################################################################################################@
# Contacts Viewset
# ####################################################################################################@

class ContactViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        member_id = User.objects.only('id').get(id=user.id)
        return ContactList.objects.filter(user_id=member_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'username_to_add': self.request.POST.getlist('username_to_add'),
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactSerializer
        elif self.request.method == 'POST':
            return AddContactRequestSerializer
        return HideContactSerializer


class ContactAcceptViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        print(contact_requests)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'username_to_accept': self.request.POST.getlist('username_to_accept')
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactRequestSerializer
        elif self.request.method == 'POST':
            return AcceptContactSerializer
        return HideContactSerializer


class ContactDeclineViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        print(contact_requests)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'username_to_decline': self.request.POST.getlist('username_to_decline')
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactRequestSerializer
        elif self.request.method == 'POST':
            return DeclineContactSerializer
        return HideContactSerializer


class ContactDeleteViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        print(contact_requests)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'username_to_delete': self.request.POST.getlist('username_to_delete')
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeleteContactSerializer
        return HideContactSerializer


# ####################################################################################################@
# Invitation Viewset
# ####################################################################################################@

class InvitationViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateInvitationsSerializer
        elif self.request.method == 'GET':
            return InvitationsSerializer
        elif self.request.method == 'POST':
            return AddInvitationsSerializer
        return HideInvitationsSerializer

    def get_queryset(self):
        member = User.objects.get(id=self.request.user.id)
        try:
            event = Event.objects.prefetch_related('creator').get(id=self.kwargs['event_pk'])
            # A member can see the invitations of an event he created
            if member.id == event.creator.id:
                return Invitation.objects.filter(event_id=self.kwargs['event_pk'])
            # A member can see the invitations of an event he is invited to
            for invitation in event.invited.all():
                if member.id == invitation.member_invited.id:
                    return Invitation.objects.filter(event_id=self.kwargs['event_pk'])
        except Event.DoesNotExist:
            print('Event doesnt exist')

    def update(self, request, *args, **kwargs):
        active_user = User.objects.get(id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['event_pk'])
        if getattr(event, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            event._prefetched_objects_cache = {}

        for invitation in event.invited.all():
            # Only the invited member can modify the status of its own invitation
            if active_user.id == invitation.member_invited.id:
                serializer = self.get_serializer(invitation, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'event_id': self.kwargs['event_pk'],
            'user_id': self.request.user.id,
            'username_to_invite': self.request.POST.getlist('username_to_invite'),
        }


# ####################################################################################################@
# Event Viewsets
# ####################################################################################################@


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

        member_id = User.objects.only('id').get(id=user.id)
        return Event.objects.prefetch_related('creator').filter(creator_id=member_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user_id': self.request.user.id,
            'protected_event_key': self.request.POST.getlist('protected_event_key'),
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
        member = User.objects.get(id=request.user.id)
        # Get a queryset object all events to which the current active user was invited to
        events = Event.objects.prefetch_related('creator').filter(invited__member_invited=member.id)
        event_list = []
        for event in events:
            serializer = EventSerializer(event)
            # print(f"event serializer.data: {serializer.data}")
            event_list.append(serializer.data)
        # return Response(event_list)
        return Response({'events': event_list})

    def update(self, request, *args, **kwargs):
        member = User.objects.get(id=request.user.id)
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
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Overriding the delete method
    def destroy(self, request, *args, **kwargs):
        member = User.objects.get(id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['pk'])
        # Only the creator of an event can delete this event
        if member.id == event.creator.id:
            event.delete()
            return Response({'message': 'Event deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
