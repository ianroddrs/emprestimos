from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('apps.main.urls')),
]

if settings.DEBUG is False:  # Serve estáticos somente em produção
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)