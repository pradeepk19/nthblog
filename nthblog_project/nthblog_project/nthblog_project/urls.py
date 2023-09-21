"""nthblog_project URL Configuration

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
from django.urls import path
from nthblogapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.index),
    path('post_list',views.post_list,name='post_list'),
    path('<id>/<slug>/',views.post_detail, name='post_detail'),
    path('post_create/',views.post_create, name='post_create'),
    path('<id>/post_edit',views.post_edit, name='post_edit'),
    path('<id>/post_delete',views.post_delete, name='post_delete'),
    path('register',views.register_page, name='register'),
    path('',views.login_page, name='login'),
    path('logout',views.logout_page, name='logout'),
    path('like',views.like_post,name='like_post'),
    path('<id>/favourite_post',views.favourite_post, name='favourite_post'),
    path('favourites',views.post_favourite_list,name='post_favourite_list')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)







