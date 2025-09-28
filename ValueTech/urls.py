# ValueTech/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.store_home, name='home'),
    path("core/", include("core.urls")),
    path("", include("accounts.urls")),
    path("store/", include("store.urls")),
    path("orders/", include("orders.urls")),
    path("offers/", include("offers.urls")),
    path("chaining/", include("smart_selects.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
