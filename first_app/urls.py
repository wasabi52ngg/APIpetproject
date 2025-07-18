from django.contrib import admin
from django.urls import path, include, re_path
from .views import (
    RestaurantViewSet, TableViewSet, WarehouseViewSet, EmployeeViewSet,
    SupplierViewSet, ProductViewSet, InventoryViewSet, MenuViewSet,
    DishViewSet, MenuDetailViewSet, ModifierViewSet, CustomerViewSet,
    ReservationViewSet, OrderViewSet, OrderDetailViewSet, PaymentViewSet
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'tables', TableViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'dishes', DishViewSet)
router.register(r'menu-details', MenuDetailViewSet)
router.register(r'modifiers', ModifierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
