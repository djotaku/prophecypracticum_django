from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'practicumweb'

urlpatterns = [
    path('', views.home, name='home'),
    path('newprophecy/', views.new_prophecy, name="newprophecy"),
    path('<int:year>/<int:month>/<int:day>/<str:prophet>/<str:supplicant>/<str:status>/', views.detailed_prophecy,
         name='detailed_prophecy'),
    path('newfeedback/', views.new_feedback, name="newfeedback"),
]
