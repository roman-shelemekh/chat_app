from django.contrib.auth import views as auth_views
from django.urls import path
from chat import views


app_name = 'chat'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('chat/<slug:slug>/', views.RoomView.as_view(), name='room'),
    path('chat/<slug:slug>/history', views.RoomHistoryView.as_view(), name='history'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', views.MyLoginView.as_view(), name='login')
]