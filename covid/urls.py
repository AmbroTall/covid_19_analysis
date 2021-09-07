from django.urls import path
from .views import side_bar_data, map_bar_data


app_name='covid'
urlpatterns = [
    path('covid19', side_bar_data, name="dashboard" ),
    path('selectCountry',  map_bar_data, name="graphs" ),
]