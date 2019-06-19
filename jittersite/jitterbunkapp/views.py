from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Bunk
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = 'jitterbunkapp/index.html'
    context_object_name = 'latest_bunks'

    def get_queryset(self):
        """Return the latest 10 bunks."""
        return Bunk.objects.order_by('-bunk_date')[:10]

    def get_context_data(self, **kwargs):
        """Add all users to context"""
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.filter(
            ~Q(id = self.request.user.id))
        return context


class BunkView(generic.DetailView):
    model = Bunk
    template_name = 'jitterbunkapp/bunkdetail.html'


class UserListView(generic.ListView):
    template_name = 'jitterbunkapp/userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        """Return the latest 10 users."""
        return User.objects.order_by('-date_joined')[:10]


class UserView(generic.DetailView):
    model = User
    template_name = 'jitterbunkapp/userdetail.html'

    def get_context_data(self, **kwargs):
        """Add all sent and received bunks to context"""
        # Call the base implementation first to get a context
        context = super(UserView, self).get_context_data(**kwargs)
        user = context['user']
        context['sent_bunks'] = Bunk.objects.filter(from_user=user.id)
        context['received_bunks'] = Bunk.objects.filter(to_user=user.id)
        return context


def create_bunk(request):
    from_user = request.user
    to_user = get_object_or_404(User, pk=request.POST['to_user_id'])
    try:
        new_bunk = Bunk(from_user=from_user, to_user=to_user)
        new_bunk.save()
    except:
        return render(request, 'jitterbunkapp/index.html', {
            'error_message': 'Failed to bunk.',
        })
    else:
        return HttpResponseRedirect(reverse('jitterbunk:index'))


def delete_bunk(request, pk):
    bunk = get_object_or_404(Bunk, pk=pk)
    try:
        bunk.delete()
    except:
        return render(request, 'jitterbunkapp/bunkdetail.html', {
            'bunk': bunk,
            'error_message': 'Failed to delete bunk.',
        })
    else:
        return HttpResponseRedirect(reverse('jitterbunk:index'))
