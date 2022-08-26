from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common.error_log import server_error_display

handler500 = server_error_display

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
