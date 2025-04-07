from django.urls import path
from . import views

#app_name="posts"

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.user_login, name='login'),
    #path('accounts/login/',views.user_login,name='login'),
    #path('logout/', views.user_logout, name='logout'),
    path('post-question/', views.post_question, name='post_question'),
    path('question/<int:pk>/', views.view_question, name='view_question'),
    path('like-answer/<int:pk>/', views.like_answer, name='like_answer'),
]