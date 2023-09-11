from django.urls import path

from analizer.views import AnalizerView, list_modules

urlpatterns = [
    path('json/', AnalizerView.as_view(), name='json'),
    path('html/', list_modules, name='modules')
]
