from django.urls import path, re_path

from . import views

urlpatterns = (
    path(r'register/', views.Register.as_view(), name="API Register"),
    path(r'login/', views.Login.as_view(), name="API Login"),
    re_path(r'^logout/', views.Logout.as_view(), name="API Logout"),
    
    path(r'current-user/', views.CurrentUserContext.as_view(), name="Current User"),
)
