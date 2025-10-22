from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('lab/', include('laboratory_gmc.urls')),
    path('lab_xa/', include('laboratory_xa.urls')),
    path('lab_otk/', include('laboratory_otk.urls')),
    path('viewer/', include('viewer.urls')),
    path('viewer_gmc/', include('viewer_gmc.urls')),
    path('techlab/', include('techlab.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
