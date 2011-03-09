from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('simplefbapp.views',
                       url('^$', 'canvas', name='fb-canvas'),
                       url('^news', 'news', name='fb-news'),
                       url('^friends', 'friends', name='fb-friends'),
                       )
