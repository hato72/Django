
from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('',views.index,name='index'),
    path('country_datetime/',views.country_datetime,name='country_datetime'),
]
