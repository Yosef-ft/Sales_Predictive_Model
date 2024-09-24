from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('apis', views.SalsesDataView)

urlpatterns = [
    path('form/', views.salesFormView, name='home'),
    path('status/', views.SalesDatapredict),
    path('', include(router.urls)),  # Include the router's URLs
]
