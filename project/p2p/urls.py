from django.urls import path
from . import views

app_name = "p2p"
urlpatterns = [
    path('calculate', views.CalculateView.as_view(), name="calculate"),
]