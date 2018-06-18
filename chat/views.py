import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        pass # Отображение контента


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def index(request):
    return render(request, 'chat/index.html', {})
# Create your views here.
