# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import EventUpdate

urlpatterns = [
    url(r'^$', EventUpdate.as_view()),
]