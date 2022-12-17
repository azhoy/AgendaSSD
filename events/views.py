from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from events.models import Event

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class EventList(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = context['events'].filter(user=self.request.user)
        return context


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = "event"


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'start_date', 'end_date', 'description', 'localisation']
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'start_date', 'end_date', 'description', 'localisation']
    success_url = reverse_lazy('events')


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('events')

