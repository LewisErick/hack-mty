from django.conf.urls import include, url

urlpatterns = [
    url(r'^login/', include('client-auth.urls', namespace="client-auth")),
    url(r'', include('ratings.urls')),
    url(r'^emotion/', include('emotion.urls', namespace="emotion")),
]
