from django.contrib.auth import views as auth_views
from django.conf import settings
from django.http import HttpResponseRedirect


# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        return auth_views.login(request)
