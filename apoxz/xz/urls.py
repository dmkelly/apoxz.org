from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('xz.views',
    url(r'^$', 'main'),
    url(r'^(?P<slug>\S+)/', 'page'),
)
