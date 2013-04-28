from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.list'),

    url(r'^view$', 'main.views.view'),
    url(r'^get_all$', 'main.views.get_all'),
    url(r'^add$', 'main.views.add'),

    url(r'^api/get_doc$', 'api.views.get_doc'),
    url(r'^api/add_doc$', 'api.views.add_doc'),
    url(r'^api/list_docs$', 'api.views.list_docs'),
)
