from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'practicumweb'

urlpatterns = [
    path('', TemplateView.as_view(template_name='practicum/home.html'), name='home'),
    path('newprophecy/', views.new_prophecy, name="newprophecy")
]
