"""SmartFIC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url,patterns
from django.contrib import admin
from SmartFICApp.views import *

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^home/$', home), #Home de la app
	url(r'^$', presentacion),
	url(r'^maxmin/$', maxmin),
	url(r'^maxmin7dias/$', maxmin7dias),
	url(r'^on/$', on),
	url(r'^off/$', on),
	url(r'^ACon/$', ACon),
	url(r'^ajustes/$', ajustes),
]
