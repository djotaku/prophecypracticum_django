from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

app_name = 'practicumweb'

urlpatterns = [
    path('', views.home, name='home'),
    path('newprophecy/', views.new_prophecy, name="newprophecy"),
    path('<int:year>/<int:month>/<int:day>/<str:prophet>/<str:supplicant>/<str:status>/', views.detailed_prophecy,
         name='detailed_prophecy'),
    path('newfeedback/<int:prophecy_id>/', views.new_feedback, name="newfeedback"),
    path('randomize/', views.randomizer, name="randomize"),
    path('statuscheck/', views.status_check, name="status check"),
    path('intructions/', TemplateView.as_view(template_name='instructions.html'), name="instructions"),
]

