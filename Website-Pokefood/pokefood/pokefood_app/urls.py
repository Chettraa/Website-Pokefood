from django.urls import path
from pokefood_app import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="about/", view=views.about, name="about"),
    path(route="book/", view=views.book, name="book"),
    path(route="menu/", view=views.menu, name="menu"),
    path(route="login/", view=views.login_view, name="login"),
    path(route="register/", view=views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
]