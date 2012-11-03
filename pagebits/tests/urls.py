from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

from ..views import PageBitView, PageView

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^test/', PageBitView.as_view(), kwargs={'groups': ['testgroup'], 'template_name': 'test.html'}, name='testview'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    (r'^(?P<url>.*)$', PageView.as_view()),
)
