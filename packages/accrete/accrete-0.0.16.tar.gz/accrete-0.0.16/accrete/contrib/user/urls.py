from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('detail/', views.user_detail, name='detail'),
    path('edit/', views.user_edit, name='edit')
]
