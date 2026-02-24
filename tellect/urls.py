from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/videos/', include('apps.videos.urls')),
    path('api/pdfs/', include('apps.pdfs.urls')),
    path('api/cbt/', include('apps.cbt.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/groups/', include('apps.groups.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
