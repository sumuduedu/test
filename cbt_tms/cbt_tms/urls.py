from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('batches/', include('batches.urls')),
    path('learning/', include('learning.urls')),
    path('assessment/', include('assessment.urls')),
    path('resources/', include('resources_app.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('certification/', include('certification.urls')),
    path('', include('accounts.urls_root')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
