"""arrihu_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apps.settings.views import LoginView
from core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    url(r'^settings/', include('apps.settings.urls', namespace='settings')),
    url(r'^member/', include('apps.member.urls', namespace='member')),
    url(r'^settings/', include('apps.division.urls', namespace='div')),
    url(r'^exam/', include('apps.exam.urls', namespace='exam')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
