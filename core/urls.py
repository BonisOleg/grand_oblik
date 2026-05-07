from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
