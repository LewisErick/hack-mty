from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^empleados/', include('empleado.urls', namespace="empleado")),
    url(r'^', include('registration.urls', namespace='registration')),
]
