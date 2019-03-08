from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    path('camera/cholesterol_login/', views.cholesterol_login, name='cholesterol_login'),
    path('camera/bilirubin_login/', views.bilirubin_login, name='bilirubin_login'),
    path('camera/cataract_login/', views.cataract_login, name='cataract_login'),
    path('camera/cholesterol/', views.cholesterol_, name='cholesterol_'),
    path('camera/bilirubin/', views.bilirubin_, name='bilirubin_'),
    path('camera/cataract/', views.cataract_, name='cataract_'),
    path('logout/', views.logout, name='logout'),
    path('history/', views.history, name='history'),
    path('home/', views.search_form),
    url(r'^signup/$', views.signup),
    path('login/', views.login),
    url(r'^aadhar/$', views.aadhar),
    url(r'^aadhar2/$', views.aadhar2),
    path('about/', views.about),
    path('contact/', views.contact),
    path('login_only_redirect/', views.login_only_redirect),
    path('direct_test/', views.direct_test),
    path('diagnosis_registered/', views.diagnosis_registered),
    path('notifyform/', views.notifyform),
    path('notifyformexec/', views.notifyformexec),
    path('genform/', views.genform),
    path('gen_diagnosis/', views.gen_diagnosis),
    path('finddoctors/', views.finddoctors),
    path('diagnosis_option/', views.diagnosis_option),
    path('camera/cholesterol_login_module/', views.cholesterol_login_module),
    path('camera/bilirubin_login_module/', views.bilirubin_login_module),
    path('camera/cataract_login_module/', views.cataract_login_module),
]