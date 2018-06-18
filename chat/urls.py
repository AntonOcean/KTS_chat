from django.urls import path, include, re_path

from chat import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='index'),
    path('<slug:room_name>/', views.room, name='room')
    # url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]