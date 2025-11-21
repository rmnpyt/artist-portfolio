from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'Portfolio Dashboard'
admin.site.index_title = 'Portfolio Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('portfolio.urls')),
    path('c/', include('content.urls')),
    path('m/', include('marketing.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
