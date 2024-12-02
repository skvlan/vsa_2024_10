from django.contrib import admin
from django.urls import path

from blog.views import all_blogs, create_blog

urlpatterns = [
    path("", all_blogs, name="all_blogs"),
    path("create/", create_blog, name="create_blog"),
]
