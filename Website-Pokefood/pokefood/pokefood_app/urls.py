from django.urls import path
from pokefood_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="about/", view=views.about, name="about"),
    path(route="book/", view=views.book, name="book"),
    path(route="menu/", view=views.menu, name="menu"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('order/', views.order_view, name='order'), # New URL for the order page
    path('process_order/', views.process_order, name='process_order'), # URL for processing the order
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)