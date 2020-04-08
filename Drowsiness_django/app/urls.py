from django.urls import path
from django.conf.urls import url
from . import views
from django.http import StreamingHttpResponse
from .util import VideoCamera, gen

# URL definitions for the application. Has only two urls, the home page at 127.0.0.1:8000 (local host) and "process_form" for form submission.
urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login, name='login'),
	path('execute', lambda r: StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame'))
]