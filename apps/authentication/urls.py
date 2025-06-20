from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),  
    path('forgot/', views.forgot, name='forgot'),  
    path('signout/', views.signout, name='signout'),  
    path('auth/<str:form_type>/', views.auth, name='auth'),  
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('change/<uidb64>/<token>/', views.change, name='change'),  
    path('protected/', views.protected_view, name='protected-route'), 
    path('me/', views.current_user_view, name='current-user'),
]
