from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.main'),

    url(r'^get$', 'main.views.get'),
    url(r'^add$', 'main.views.add'),
    url(r'^list$', 'main.views.list'),

    url(r'^api/get_doc$', 'api.views.get_doc'),
    url(r'^api/add_doc$', 'api.views.add_doc'),
    url(r'^api/list_docs$', 'api.views.list_docs'),
)
