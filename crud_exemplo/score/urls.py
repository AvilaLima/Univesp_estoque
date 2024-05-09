from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('produtos/', views.produtos, name='produtos'),
    path('estoque/', views.estoque, name='estoque'),
]