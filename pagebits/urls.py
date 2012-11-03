from django.conf.urls import patterns

from .views import PageView


urlpatterns = patterns('',
    (r'^(?P<url>.*)$', PageView.as_view()),
)
