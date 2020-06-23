from django.urls import path
from .import views

# template urls
app_name = 'user_app'

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register')
]
