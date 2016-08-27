from django.conf.urls import include, url

urlpatterns = [
    url(r'^emotion/', include('emotion.urls', namespace="emotion"))
]
