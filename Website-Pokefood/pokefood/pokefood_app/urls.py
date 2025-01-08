from django.urls import path
from pokefood_app import views

urlpatterns = [
    path(route="", view=views.index, name = "index"),
    path(route="about/", view=views.about, name = "about"),
    path(route="book/", view=views.book, name = "book"),
    path(route="menu/", view=views.menu, name = "menu"),
    path(route="log_in/", view=views.log_in, name = "log_in"),
]