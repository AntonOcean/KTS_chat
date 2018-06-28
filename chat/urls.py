from django.urls import path


from chat import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='index'),
    path('login/', views.ChatLoginView.as_view(), name='login'),
    path('logout/', views.ChatLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<slug:room_name>/', views.RoomView.as_view(), name='room'),
]
