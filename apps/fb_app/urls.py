from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_new_user$', views.register_new_user),
    url(r'^login_user$', views.login_user),
    url(r'^all_books$', views.all_books),
    url(r'^add_new_book$', views.add_new_book),
    url(r'^view_book/(?P<id>\d+)$', views.view_book),
    url(r'^update_book/(?P<id>\d+)$', views.update_book),
    url(r'^delete_book/(?P<id>\d+)$', views.delete_book),
    url(r'^favorite_book/(?P<id>\d+)$', views.favorite_book),
    url(r'^unfavorite_book/(?P<id>\d+)$', views.unfavorite_book),
    url(r'^log_out_user$', views.log_out_user),
]