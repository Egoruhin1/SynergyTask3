from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Импортируем auth_views

urlpatterns = [
    path('', views.post_list, name='blog-home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog-home'), name='logout'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('subscribe/<str:username>/', views.subscribe_user, name='subscribe-user'),
    path('subscriptions/', views.subscription_posts, name='subscription-posts'),
    path('user/<str:username>/', views.user_posts, name='user-posts'),
    path('profile/', views.user_profile, name='user-profile'),  # Добавьте этот маршрут
]
