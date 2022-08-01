from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from principal import settings



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path("payments/", include("payments.urls")),
    
    ]

handler404 = "pages.views.handle_not_found"

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

