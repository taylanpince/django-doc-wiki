from django.conf.urls.defaults import *


urlpatterns = patterns('doc_wiki.views',
    url(r'^$', 'wiki_index', name="doc_wiki_index"),
    url(r'^(?P<slug>[-\w]+)/$', 'wiki_page', name="doc_wiki_page"),
    url(r'^(?P<slug>[-\w]+)/source/$', 'wiki_page_source', name="doc_wiki_page_source"),
)
