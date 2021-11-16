from django.conf.urls import url
from certificate import views

urlpatterns = [
    url(r'^api/certificates$', views.view.as_view()),
    url(r'^api/certificates/(?P<pk>[0-9]+)$', views.detail_view.as_view())
]