from django.urls import path
from . import views


urlpatterns = [
    path('', views.produtos, name='produtos'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('produtos/', views.produtos, name='produtos'),
    path('estoque/', views.estoque, name='estoque'),
    path('relatorio/', views.relatorio, name='relatorio'),
]