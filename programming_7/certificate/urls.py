from django.conf.urls import url
from certificate import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger$', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/certificates$', views.view.as_view()),
    url(r'^api/certificates/(?P<pk>[0-9]+)$', views.detail_view.as_view())
]