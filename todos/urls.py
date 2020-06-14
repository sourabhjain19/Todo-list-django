from django.urls import path, include

from . import views

urlpatterns = [
    path('loginform/', views.loginform, name="loginform"),
    path('login/', views.login, name="login"),
    path('registerform/', views.registerform, name="registerform"),
    path('register/', views.sendmail, name="sendmail"),
    path('verify/<token>/',views.register,name="register"),
    path('logout/', views.logout, name="logout"),
    path('',views.home,name="home"),
    path('addform/',views.addform,name="addform"),
    path('add/',views.add,name='add'),
    path('delete/<pk_id>',views.delete,name="delete"),
]
