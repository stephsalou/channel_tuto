from django.shortcuts import render , get_object_or_404 , Http404 ,HttpResponse
from django.views.generic import View
from .models import Message

# Create your views here
class RoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'blog/room.html')
        

    def post(self, request, *args, **kwargs):
        raise Http404('Page not found')


class homeView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'blog/index.html')

    def post(self, request, *args, **kwargs):
        raise Http404('not found')