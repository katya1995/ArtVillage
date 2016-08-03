from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth

urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^index/', include('TheArtVillage.urls')),
                       url(r'^', include('TheArtVillage.urls')),
                       )

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
