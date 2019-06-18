from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Bunk, User

class IndexView(generic.ListView):
    template_name = 'jitterbunkapp/index.html'
    context_object_name = 'latest_bunks'

    def get_queryset(self):
        """Return the latest 10 bunks."""
        return Bunk.objects.filter(
            bunk_date__lte=timezone.now()
        ).order_by('-bunk_date')[:10]

    def get_context_data(self, **kwargs):
        """Add users to context"""
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.filter(signup_date__lte=timezone.now())
        return context


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


def create_user(request):
    try:
        username = request.POST['username']
        new_user = User(username=username, signup_date=timezone.now())
        new_user.save()
    except:
        return render(request, 'jitterbunkapp/userlist.html', {
            'error_message': "Failed to create user.",
        })
    else:
        return HttpResponseRedirect(reverse('jitterbunk:userlist'))


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        user.delete()
    except:
        return render(request, 'jitterbunkapp/userdetail.html', {
            'user': user,
            'error_message': "Failed to delete user.",
        })
    else:
        return HttpResponseRedirect(reverse('jitterbunk:userlist'))


def create_bunk(request):
    from_user = get_object_or_404(User, pk=request.POST['from_user_id'])
    to_user = get_object_or_404(User, pk=request.POST['to_user_id'])
    try:
        new_bunk = Bunk(from_user=from_user, to_user=to_user, bunk_date=timezone.now())
        new_bunk.save()
    except:
        return render(request, 'jitterbunkapp/index.html', {
            'error_message': "Failed to bunk.",
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
            'error_message': "Failed to delete bunk.",
        })
    else:
        return HttpResponseRedirect(reverse('jitterbunk:index'))
