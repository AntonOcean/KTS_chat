import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView, CreateView
from django.http import HttpResponseRedirect

from django.views.generic.base import View
from django.views.generic.list import BaseListView

from chat.forms import ChatLoginForm, ChatCreationForm
from chat.models import Message, Room


class ChatView(LoginRequiredMixin,TemplateView):
    # create and redirect room or select chat in future
    template_name = 'chat/index.html'
    # login_url = 'login/'
    def get_login_url(self):
        return reverse('chat:login')

# BaseListView
#render to response
#content type
# последнее сообщение ласт мессадж айди
# jquery ajax GET room_id last,_message_id


# class MessageView(BaseListView):
#     model = Message
#     paginate_by = 5
#
#     # def get_queryset(self):
#     #     pass
#
#     def get(self, request, *args, **kwargs):
#         context = super().get_context_data()
#         return self.render_to_response(context)



class RoomView(LoginRequiredMixin,TemplateView):
    template_name = 'chat/room.html'
    # login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = context.get('room_name')
        print(room_name)

        # брать сообщения из базы и выкидывать как messages
        # как делать пагинацию на уровне ajax?
        # бесконечная прокрутка  с подгрузкой
        room = Room.objects.get_or_create(name=room_name)
        messages = room[0].message_set.all()
        # print(messages[0].author.avatar)
        messages_date = (m.to_json() for m in messages)

        print('this message in view', messages_date)
        context['room_name_json'] = mark_safe(json.dumps(room_name))

        context['messages'] = messages_date
        return context

    def get_login_url(self):
        return reverse('chat:login')


class ChatLoginView(LoginView):
    template_name = 'form.html'
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


# как сюда не заходить лишний раз
class RegisryView(FormView):
    form_class = ChatCreationForm
    template_name = "form.html"

    def get(self, request, *args, **kwargs):
        # print(request.user)
        if request.user.is_authenticated:
            url = reverse('chat:index')
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chat:index')

# class MessageCreateView(FormView):
#     form_class = MessageCreateForm
#
#     def get_success_url(self):
#         return reverse('chat:index')