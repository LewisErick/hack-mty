from django.conf.urls import include, url

urlpatterns = [
    url(r'^login/', include('client-auth.urls', namespace="client-auth")),
    url(r'^emotion/', include('emotion.urls', namespace="emotion")),
    url(r'', include('ratings.urls')),
]
