from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from .views import ApiHomeView, RootHomeView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def health_check(request):
    return JsonResponse({"status": "ok"})

def ready_check(request):
    return JsonResponse({"status": "ready"})

urlpatterns = [
    path('', RootHomeView.as_view(), name='root-home'),
    path('health/', health_check, name='health_check'),
    path('ready/', ready_check, name='ready_check'),
    path('admin/', admin.site.urls),
    path('api/', ApiHomeView.as_view(), name='api-home'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/videos/', include('apps.videos.urls')),
    path('api/pdfs/', include('apps.pdfs.urls')),
    path('api/cbt/', include('apps.cbt.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/groups/', include('apps.groups.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/certificates/', include('apps.certificates.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/announcements/', include('apps.announcements.urls')),
    path('api/support/', include('apps.support.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
