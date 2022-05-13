from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('change/password/', views.change_password, name='change_password'),
    path('forgot/password/', views.forgot_password, name='forgot_password'),
    path('reset/<int:id>/', views.reset_password, name='reset_password'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('logout/', views.logout, name="logout"),
]
