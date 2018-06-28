import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView, CreateView
from django.http import HttpResponseRedirect, JsonResponse

from django.views.generic.base import View
from django.views.generic.list import BaseListView, ListView, MultipleObjectMixin

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




class MessageView(ListView):
    model = Message
    paginate_by = 20

    template_name = 'chat/message_test.html'
#

    # def render_to_response(self):


    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     # print(context)
    #     # context['object_list'] = json.dumps(context['object_list'])
    #     # print(context['object_list'])
    #     # print('see it again', context)
    #     print(context['object_list'])
    #     return render_to_response(template_name='chat/message_test.html', context=context)
        # return JsonResponse(context=context, dta)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # filter by room id
    #     object_list = [m.to_json_v2() for m in Message.objects.all()]
    #     print(type(object_list))
    #     print(object_list)
    #     return super().get_context_data(object_list=object_list, **kwargs)
    # def get_queryset(self):
    #     pass
    #
    # def get(self, request, *args, **kwargs):
    #     context = super().get_context_data()
    #     return self.render_to_response(context)


class RoomView(LoginRequiredMixin, ListView):
    template_name = 'chat/room.html'
    paginate_by = 5
    model = Message
    context_object_name = 'messages'

    def get_context_data(self, *, object_list=None, **kwargs):
        room_name = self.kwargs.get('room_name')
        print(self.kwargs)
        print(room_name)

        # брать сообщения из базы и выкидывать как messages
        # как делать пагинацию на уровне ajax?
        # бесконечная прокрутка  с подгрузкой
        room = Room.objects.get_or_create(name=room_name)
        messages = room[0].message_set.order_by('-date').all()
        messages_date = [m.to_json() for m in messages]

        print('this message in view', messages_date)
        room_name_json = mark_safe(json.dumps(room_name))

        # context['object_list'] = messages_date
        return super().get_context_data(object_list=messages_date, room_name_json=room_name_json, **kwargs)

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


class RegisryView(FormView):
    form_class = ChatCreationForm
    template_name = "form.html"

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

