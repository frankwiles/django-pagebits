from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

from ..views import PageBitView

urlpatterns = patterns('',
        (r'^admin/', include(admin.site.urls)),
        url(r'^test/', PageBitView.as_view(), kwargs={'groups': ['testgroup'], 'template_name': 'test.html'}, name='testview'),
)
