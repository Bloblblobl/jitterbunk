from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone

from .models import Bunk, User

class IndexView(generic.ListView):
    template_name = 'jitterbunkapp/index.html'
    context_object_name = 'latest_bunks'

    def get_queryset(self):
        """Return the latest 10 bunks."""
        return Bunk.objects.filter(
            bunk_date__lte=timezone.now()
        ).order_by('-bunk_date')[:10]


class BunkView(generic.DetailView):
    model = Bunk
    template_name = 'jitterbunkapp/bunkdetail.html'

    def get_queryset(self):
        """Exclude future bunks."""
        return Bunk.objects.filter(bunk_date__lte=timezone.now())


class UserListView(generic.ListView):
    template_name = 'jitterbunkapp/userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        """Return the latest 10 users."""
        return User.objects.filter(
            signup_date__lte=timezone.now()
        ).order_by('-signup_date')[:10]


class UserView(generic.DetailView):
    model = User
    template_name = 'jitterbunkapp/userdetail.html'

    def get_queryset(self):
        """Exclude future users."""
        return User.objects.filter(signup_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        """Add all sent and received bunks to context"""
        # Call the base implementation first to get a context
        context = super(UserView, self).get_context_data(**kwargs)
        user = context['user']
        context['sent_bunks'] = Bunk.objects.filter(from_user=user.id)
        context['received_bunks'] = Bunk.objects.filter(to_user=user.id)
        return context
