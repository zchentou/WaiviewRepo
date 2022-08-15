"""HumanityUnited URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages import views as page_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_views.home_view, name='home'),
    path('about/', page_views.about_view, name='about'),
    path('contact/', page_views.contact_view, name='contact'),
    path('privacy/', page_views.privacy_policy_view, name='privacy'),
    path('terms/', page_views.terms_of_use_view, name='terms-of-use'),
    path('sitemap.xml/', page_views.sitemap_view, name='sitemap'),
    path('acknowledgments/', page_views.acknowledgments_view, name='acknowledgments'),
    path('usersearch/', page_views.UserListView.as_view(template_name='pages/user_list.html'), name='user-search'),
    path('stories/', include('stories.urls')),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
    path('artworks/', include('artworks.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
