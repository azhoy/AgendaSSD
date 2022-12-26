from django_filters.rest_framework import FilterSet
from .models import Event, Member


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = {
            'id': ['exact']
        }


class MemberFilter(FilterSet):
    class Meta:
        model = Member
        fields = {
            'id': ['exact']
        }
