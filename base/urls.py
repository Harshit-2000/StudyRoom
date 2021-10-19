from django.urls import path
from . import views

urlpatterns = [

    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),

    path('', views.home_view, name="home"), 
    path('room/<str:pk>', views.room_view, name="room"),

    path('create-room/', views.create_room_view, name="create-room"),
    path('update-room/<str:pk>', views.update_room_view, name="update-room"),
    path('delete-room/<str:pk>', views.delete_room_view, name="delete-room"),

    path('delete-message/<str:pk>', views.delete_message_view, name="delete-message"),   

    path('profile/<str:pk>', views.user_profile_view, name = 'user-profile'),
]
