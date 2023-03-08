from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter

from creditcard.api import CreditcardViewSet

router = DefaultRouter()
router.register(r'creditcards', CreditcardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin', permanent=False)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
