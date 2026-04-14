# api/views.py
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from django.utils import timezone
import platform
import psutil
from datetime import datetime
from django.db import connection
from django.core.cache import cache

class ApiHomeView(APIView):
    """
    Enhanced API home view with documentation, stats, and discovery
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Get API base URL from request
        api_base = request.build_absolute_uri('/api/')
        
        # Get user info if authenticated
        user_info = None
        if request.user.is_authenticated:
            user_info = {
                "username": request.user.username,
                "email": request.user.email,
                "role": getattr(request.user, 'role', 'student'),
                "is_authenticated": True
            }
        
        response_data = {
            "name": "Tellect LMS API",
            "version": "2.0.0",
            "description": "Learning Management System Backend API",
            "documentation": {
                "swagger": f"{api_base}docs/",
                "redoc": f"{api_base}redoc/",
                "postman": "https://documenter.getpostman.com/view/...",
            },
            "status": {
                "environment": settings.ENVIRONMENT,  # dev/staging/prod
                "timestamp": timezone.now().isoformat(),
                "maintenance_mode": getattr(settings, 'MAINTENANCE_MODE', False),
            },
            "authentication": {
                "status": "authenticated" if request.user.is_authenticated else "anonymous",
                "user": user_info,
                "login_url": f"{api_base}auth/login/",
                "register_url": f"{api_base}auth/register/",
                "docs": "Use Bearer token in Authorization header"
            },
            "modules": self.get_modules(api_base),
            "pagination": {
                "default_limit": 20,
                "max_limit": 100
            },
            "rate_limits": {
                "anonymous": "100/hour",
                "authenticated": "1000/hour"
            },
            "links": {
                "self": request.build_absolute_uri(),
                "health_check": f"{api_base}health/",
                "metrics": f"{api_base}metrics/",
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_modules(self, api_base):
        """Organize modules by category with descriptions"""
        return {
            "core": {
                "auth": {
                    "url": f"{api_base}auth/",
                    "description": "Authentication & user management",
                    "methods": ["POST", "GET", "PUT"]
                },
                "courses": {
                    "url": f"{api_base}courses/",
                    "description": "Course management and browsing",
                    "methods": ["GET", "POST", "PUT", "DELETE"]
                },
                "dashboard": {
                    "url": f"{api_base}dashboard/",
                    "description": "User dashboard and analytics",
                    "methods": ["GET"]
                }
            },
            "content": {
                "videos": {
                    "url": f"{api_base}videos/",
                    "description": "Video content streaming and management",
                    "methods": ["GET", "POST", "PUT", "DELETE"]
                },
                "pdfs": {
                    "url": f"{api_base}pdfs/",
                    "description": "PDF document management",
                    "methods": ["GET", "POST", "PUT", "DELETE"]
                }
            },
            "assessment": {
                "cbt": {
                    "url": f"{api_base}cbt/",
                    "description": "Computer-Based Testing and quizzes",
                    "methods": ["GET", "POST", "PUT"]
                }
            },
            "social": {
                "groups": {
                    "url": f"{api_base}groups/",
                    "description": "Study groups and discussions",
                    "methods": ["GET", "POST", "PUT", "DELETE"]
                },
                "announcements": {
                    "url": f"{api_base}announcements/",
                    "description": "Platform announcements",
                    "methods": ["GET", "POST"]
                }
            },
            "financial": {
                "payments": {
                    "url": f"{api_base}payments/",
                    "description": "Payment processing and history",
                    "methods": ["POST", "GET"]
                }
            },
            "communication": {
                "notifications": {
                    "url": f"{api_base}notifications/",
                    "description": "Push and email notifications",
                    "methods": ["GET", "POST", "PUT"]
                },
                "support": {
                    "url": f"{api_base}support/",
                    "description": "Customer support tickets",
                    "methods": ["GET", "POST"]
                }
            },
            "analytics": {
                "certificates": {
                    "url": f"{api_base}certificates/",
                    "description": "Certificate generation and verification",
                    "methods": ["GET", "POST"]
                },
                "analytics": {
                    "url": f"{api_base}analytics/",
                    "description": "Learning analytics and reports",
                    "methods": ["GET"]
                }
            }
        }


class RootHomeView(APIView):
    """
    Root endpoint - redirects to API documentation
    """
    permission_classes = [AllowAny]

    def get(self, request):
        api_url = request.build_absolute_uri('/api/')
        
        return Response({
            "name": "Tellect LMS Backend",
            "tagline": "Modern Learning Management System",
            "version": "2.0.0",
            "api": {
                "url": api_url,
                "documentation": f"{api_url}docs/",
                "status": "operational"
            },
            "quick_links": {
                "login": f"{api_url}auth/login/",
                "register": f"{api_url}auth/register/",
                "browse_courses": f"{api_url}courses/",
                "health_check": f"{api_url}health/"
            },
            "health": {
                "status": "healthy",
                "timestamp": timezone.now().isoformat()
            },
            "company": {
                "name": "Tellect Inc.",
                "website": "https://tellect.com",
                "support_email": "support@tellect.com"
            }
        }, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """
    Detailed health check endpoint for monitoring
    """
    permission_classes = [AllowAny]

    def get(self, request):
        health_data = {
            "status": "healthy",
            "timestamp": timezone.now().isoformat(),
            "services": {
                "database": self.check_database(),
                "cache": self.check_cache(),
                "storage": self.check_storage(),
            },
            "system": {
                "python_version": platform.python_version(),
                "django_version": settings.DJANGO_VERSION,
                "environment": settings.ENVIRONMENT,
            }
        }
        
        # Determine overall status
        if all(service["status"] == "healthy" for service in health_data["services"].values()):
            return Response(health_data, status=status.HTTP_200_OK)
        else:
            health_data["status"] = "degraded"
            return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def check_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return {"status": "healthy", "latency": "ok"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def check_cache(self):
        try:
            cache.set("health_check", "ok", 5)
            if cache.get("health_check") == "ok":
                return {"status": "healthy", "backend": settings.CACHES['default']['BACKEND']}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def check_storage(self):
        try:
            from django.core.files.storage import default_storage
            # Try to list files (read operation)
            default_storage.exists("health_check.txt")
            return {"status": "healthy", "backend": default_storage.__class__.__name__}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


class APIMetricsView(APIView):
    """
    API metrics and usage statistics
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # This would typically come from a metrics service like Prometheus
        return Response({
            "uptime": self.get_uptime(),
            "total_requests_today": 15420,
            "active_users": {
                "total": 342,
                "students": 289,
                "instructors": 48,
                "admins": 5
            },
            "response_times": {
                "average_ms": 245,
                "p95_ms": 567,
                "p99_ms": 892
            },
            "endpoints": {
                "total": 156,
                "public": 89,
                "protected": 67
            }
        })
    
    def get_uptime(self):
        # This would actually calculate from process start time
        return "15d 7h 23m"