import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from chat.forms import ChatLoginForm, ChatUserCreationForm
from chat.models import Message, Room


class ChatView(LoginRequiredMixin,TemplateView):
    template_name = 'chat/index.html'

    def get_login_url(self):
        return reverse('chat:login')


class RoomView(LoginRequiredMixin, ListView):
    template_name = 'chat/room.html'
    paginate_by = 5
    model = Message
    context_object_name = 'messages'

    def get_context_data(self, *, object_list=None, **kwargs):
        room_name = self.kwargs.get('room_name')
        room = Room.objects.get_or_create(name=room_name)
        messages = room[0].message_set.order_by('-date').all()
        messages_date = [m.to_json() for m in messages]
        room_name_json = mark_safe(json.dumps(room_name))
        return super().get_context_data(object_list=messages_date, room_name_json=room_name_json, **kwargs)

    def get_login_url(self):
        return reverse('chat:login')


class ChatLoginView(LoginView):
    template_name = 'chat/signin.html'
    form_class = ChatLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('chat:login')
        return data

    def get_success_url(self):
        return reverse('chat:index')


class ChatLogoutView(LogoutView):
    pass


class SignUpView(FormView):
    form_class = ChatUserCreationForm
    template_name = "chat/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            url = reverse('chat:index')
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chat:index')

