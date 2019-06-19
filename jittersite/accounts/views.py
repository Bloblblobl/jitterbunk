from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
