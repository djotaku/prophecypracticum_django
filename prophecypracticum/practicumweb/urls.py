from django.urls import path
from . import views

app_name = 'practicumweb'

urlpatterns = [
    path('newprophecy/', views.new_prophecy, name="newprophecy")
]
