from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views


# all the urls pattern in the inspyme app
urlpatterns = [
    path("", views.home, name='home'),
    path("stories", views.mystory, name='mystory'),
    path("login/", views.login_page, name='login_page'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("signup/", views.signup, name='signup'),
    path("addstory/", views.addstory, name='addstory'),
    path("story/comment/<int:id>", views.addcomment, name='addcomment'),
    path("delete/comment/<int:id>", views.deletecomment, name='deletecomment'),
    path("delete/story/<int:id>", views.deletestory, name='deletestory'),
    path("edit/story/<int:id>", views.editstory, name='editstory'),
    path("edit/comment/<int:id>", views.editcomment, name='editcomment'),
    path("edit/profile/<int:id>", views.editaccount, name='editaccount'),
    path('accounts/login/', LoginView.as_view(), name='login'),
]