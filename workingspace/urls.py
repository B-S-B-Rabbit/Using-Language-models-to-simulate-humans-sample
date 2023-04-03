from django.urls import path
from . import views
from .views import MyLoginView, LogoutView, ProfileView

urlpatterns = [
    path('', views.home, name='home'),
    path('project/', views.project, name='project'),
    path('register/sign-up', views.register_s_i, name='register\sign-up'),
    path('register/login', MyLoginView.as_view(template_name='registration_l_i.html'), name='register\login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
