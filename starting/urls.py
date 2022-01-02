from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("room/<str:id>/",views.room,name="room"),
    path("create_room/",views.create_room,name="create_room"),
    path("update_room/<str:id>/",views.update_room,name="update_room"),
    path("delete_room/<str:id>/",views.delete_room,name="delete_room"),
    path("login_page/",views.login_page,name="login_page"),
    path("logout_user/",views.logout_user,name="logout_user"),
    path("register/",views.register_page,name="register"),
    path("delete_message/<str:id>/",views.delete_message,name="delete_message"),
    path("update_message/<str:id>/",views.update_message,name="update_message"),
    path("profile/<str:id>/",views.profile,name="profile"),
]