from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('project/', views.project, name='project'),
    path('register/', views.register_s_i, name='register\sign-in'),
]
