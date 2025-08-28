from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def api_root(_request):
    return JsonResponse({
        "name": "Social Media API",
        "status": "ok",
        "endpoints": {
            "register": "/api/accounts/register",
            "login": "/api/accounts/login",
            "profile": "/api/accounts/profile"
        }
    })

urlpatterns = [
    path("", api_root, name="api-root"),            # ← add this
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
