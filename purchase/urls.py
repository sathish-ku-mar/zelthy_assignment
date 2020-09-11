# from django.urls import path,include
from django.conf.urls import url

from .views import PurchaseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PurchaseViewSet)


urlpatterns = [
    # path(r'search/', MovieViewSet.as_view({'post': 'search'}), name='search'),
]

urlpatterns += router.urls