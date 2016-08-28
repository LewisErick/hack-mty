from django.contrib.auth import views as auth_views
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.generic.base import TemplateView

# Create your views here.
class LoginView(TemplateView):
	template_name = "registration/login.html"

	def post(self, request, *args, **kwargs):
		print(request.body)
		next = request.GET.get('next', '/')
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					print("User is valid, active and authenticated")
					login(request, user)
					return HttpResponseRedirect(next)
				else:
					print("The password is valid, but the account has been disabled!")
					return HttpResponse("Usuario desactivado")
					## TODO (4) Utilizar un form para que se devuelva el error a la pantalla template
			else:
				print("The username and password were incorrect.")
				return HttpResponseRedirect(settings.LOGIN_URL)

		return render(request, "account/login.html", {'redirect_to': next})

	#class LogoffAuth():		
	def Logout(request):
		logout(request)
		return HttpResponseRedirect(settings.LOGIN_URL)
