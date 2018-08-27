from django.conf.urls import url
from User.views import phone_valid, register

urlpatterns = [
    url(r'^phone_valid/$', phone_valid),
    url(r'^register/$', register),
]