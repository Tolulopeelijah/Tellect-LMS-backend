from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ApiHomeView, RootHomeView, HealthCheckView, APIMetricsView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def ready_check(request):
    from django.http import JsonResponse
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return JsonResponse({'status': 'ready'})
    except Exception as exc:
        return JsonResponse({'status': 'not_ready', 'error': str(exc)}, status=503)


urlpatterns = [
    path('', RootHomeView.as_view(), name='root-home'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('ready/', ready_check, name='ready_check'),
    path('admin/', admin.site.urls),
    path('api/', ApiHomeView.as_view(), name='api-home'),
    path('api/metrics/', APIMetricsView.as_view(), name='api-metrics'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
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
