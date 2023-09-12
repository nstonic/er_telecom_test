from django.urls import path

from analizer.views import analize, list_modules

urlpatterns = [
    path('json/', analize, name='json'),
    path('html/', list_modules, name='modules')
]
