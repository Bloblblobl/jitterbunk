from django.conf.urls import url

from . import views

app_name = 'jitterbunk'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^bunk/$', views.create_bunk, name='create_bunk'),
    url(r'^(?P<pk>[0-9]+)/$', views.BunkView.as_view(), name='bunk'),
    url(r'^users/$', views.UserListView.as_view(), name='userlist'),
    url(r'^users/create/$', views.create_user, name='create_user'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user'),
]
