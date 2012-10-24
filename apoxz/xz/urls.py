from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('xz.views',
    url(r'^$', 'main'),
)
