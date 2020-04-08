from django.shortcuts import render
from .util import *
from django.db.models.base import ObjectDoesNotExist
from .models import Auth
from django.http import HttpResponse

def index(request):
	try:
		response = getCookie(request)

		print (response)

		if response == "true":
			return render(request, 'dashboard.html', {'auth':True})

	except KeyError:
		return render(request, 'index.html')

def login(request):

	username = request.POST.get('username', '')
	password = request.POST.get('password', '')

	try:
		userdata = Auth.objects.get(username_db = username)
		userdata = Auth.objects.get(password_db = password)

		setCookie(request)

		return render(request, 'dashboard.html', {'auth':True})

	except ObjectDoesNotExist:
		return render(request, 'dashboard.html', {'auth':False})