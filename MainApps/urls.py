from django.contrib import admin
from django.urls import path, include, re_path as url
from django.conf.urls import handler404, handler500
from . import views

urlpatterns = [
    path('', views.index, name='index_mysite'),

    path('daftar/', views.daftar, name='daftar'),
    path('akun/', views.akun, name='akun'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('siwarkah/', include('siwarkah.urls')),
    path('sipekat/', include('sipekat.urls')),

    path('admin/', admin.site.urls),
]

handler404 = 'sipekat.views.error_404'
handler500 = 'sipekat.views.error_500'