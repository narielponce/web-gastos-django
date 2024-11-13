from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IntegranteFamiliaViewSet, CategoriaViewSet, MetodoPagoViewSet, TransaccionViewSet, CuotaViewSet
from . import views

router = DefaultRouter()
# router.register(r'familias', FamiliaViewSet)
router.register(r'integrantes', IntegranteFamiliaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'metodos_pago', MetodoPagoViewSet)
router.register(r'transacciones', TransaccionViewSet)
router.register(r'cuotas', CuotaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cargar-transaccion/', views.cargar_transaccion, name='cargar_transaccion'),
    path('transacciones-web/', views.lista_transacciones, name='lista_transacciones'),  # Suponiendo que lista_transacciones ya existe
    path('dashboard/', views.dashboard, name='dashboard'),
    path('informe-uno/', views.gastos_ingresos, name='informe1'),
    path('informe-compras-tarjeta/', views.informe_compras_tarjeta, name='informe_compras_tarjeta'),
]
