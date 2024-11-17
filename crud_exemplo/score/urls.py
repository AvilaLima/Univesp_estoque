from django.urls import path
from . import views


urlpatterns = [
    path("", views.produtos, name="produtos"),
    path("funcionarios/", views.funcionarios, name="funcionarios"),
    path("produtos/", views.produtos, name="produtos"),
    path("estoque/", views.estoque, name="estoque"),
    path("relatorio/", views.relatorio, name="relatorio"),
    path("estoque/webcam/", views.exibir_webcam, name="exibir_webcam"),
    path("processar_estoque/", views.processar_estoque, name="processar_estoque"),
    path(
        "process_barcode_image/",
        views.process_barcode_image,
        name="process_barcode_image",
    ),
]
