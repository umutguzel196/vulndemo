from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sql/', views.sql_vulnerable),
    path('xss/', views.xss_vulnerable),
    path('csrf/', views.csrf_vulnerable),
    path('session/', views.session_fixation_login),
    path('idor/', views.idor_vulnerable),
    path('clickjacking/', views.clickjacking_vulnerable),
]