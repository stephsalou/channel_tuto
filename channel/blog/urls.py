from django.urls import path
from .views import RoomView , homeView

urlpatterns = [
    path("room/", RoomView.as_view(), name="edit_art"),
    path('', homeView.as_view(), name='home'),
]

