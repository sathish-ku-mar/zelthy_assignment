# from django.urls import path,include
from django.conf.urls import url

from .views import PurchaseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PurchaseViewSet)


urlpatterns = [
    url(r'filter/', PurchaseViewSet.as_view({'post': 'filter'}), name='filter'),
]

urlpatterns += router.urls