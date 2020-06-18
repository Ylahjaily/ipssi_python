from django.urls import path, re_path
from webapp import views

app_name = 'webapp'

urlpatterns = [
    path('', views.webapp_index, name='webapp_index'),
    path('annonces/offres', views.webapp_annonces_offres, name='webapp_annonce_offres'),
    path('annonces/new', views.webapp_annonce_new, name='webapp_annonce_new'),
    path('annonces/requests', views.webapp_annonces_requests, name='webapp_annonces_requests'),
    path('annonces/offres/search', views.webapp_annonces_offres_search, name='webapp_annonces_offres_search'),
    path('annonces/requests/search', views.webapp_annonces_requests_search, name='webapp_annonces_requests_search'),
    re_path('annonces/(?P<uuid>[\w-]+)/$', views.webapp_annonce, name='webapp_annonce'),
    path('login', views.webapp_login, name='webapp_login'),
    path('register', views.webapp_register, name='webapp_register'),
    path('logout', views.webapp_logout, name='webapp_logout'),
    path('profile', views.webapp_profile, name='webapp_profile'),
    re_path('annonces/conversation/new/(?P<uuid>[\w-]+)/$', views.webapp_conversation_start,
            name='webapp_conversation_start'),
    re_path('annonces/message/new/(?P<uuid>[\w-]+)/$', views.webapp_new_message, name='webapp_new_message')
]
