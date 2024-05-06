from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter(trailing_slash=False)
router.register(r'purchase_orders', PurchaseViewset)
router.register(r'vendors', VendorViewset)
router.register(r'history', HistoryViewset)

urlpatterns = router.urls

urlpatterns += [
    path("token", obtain_auth_token),
    path("users", UserViewset.as_view()),
    path("users/<username>", UserViewset.as_view())
]