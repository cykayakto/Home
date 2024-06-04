from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
def check_admin(user):
   return user.is_superuser

# Create your views here.
@user_passes_test(check_admin)
def index(request):
	return render(request, 'admin_panel/index.html')