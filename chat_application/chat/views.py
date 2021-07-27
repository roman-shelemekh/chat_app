from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from .forms import RoomEnterForm, RoomCreateForm, SignUpForm, LoginForm
from .models import RoomModel


class IndexView(TemplateView):
    template_name = 'chat/index.html'

    def dispatch(self, request, *args, **kwargs):
        self.enter_form = RoomEnterForm()
        self.create_form = RoomCreateForm()
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('button') == 'create':
            self.create_form = RoomCreateForm(request.POST)
            if self.create_form.is_valid():
                room_name = self.create_form.cleaned_data['room_name']
                room_password = self.create_form.cleaned_data['room_password1']
                room = RoomModel.objects.create_room(room_name, room_password)
                request.session[room_name] = True
                return HttpResponseRedirect(reverse('chat:room', args=[room.slug]))
            else:
                self.create_form.validation_error_class()
        elif request.POST.get('button') == 'enter':
            self.enter_form = RoomEnterForm(request.POST)
            if self.enter_form.is_valid():
                room_name = self.enter_form.cleaned_data.get('room_name')
                room = RoomModel.objects.get(room_name=room_name)
                request.session[room_name] = True
                return HttpResponseRedirect(reverse('chat:room', args=[room.slug]))
            else:
                self.enter_form.validation_error_class()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'enter_form': self.enter_form, 'create_form': self.create_form})
        return context


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'chat/signup.html'

    def get_success_url(self):
        return reverse('chat:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        form.validation_error_class()
        return super(SignupView, self).form_invalid(form)


class MyLoginView(LoginView):
    template_name = 'chat/login.html'
    form_class = LoginForm

    def form_invalid(self, form):
        form.validation_error_class()
        return super(MyLoginView, self).form_invalid(form)


class RoomAuthMixin:
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        room = self.get_object(queryset=RoomModel.objects.all())
        if not request.session.get(room.room_name):
            messages.warning(request, 'К сожалению, у Вас нет доступа к этому чату. Вы можете к нему '
                                      'присоединиться, введя нужный пароль')
            return HttpResponseRedirect(reverse('chat:index'))
        else:
            return response


class RoomView(RoomAuthMixin, LoginRequiredMixin, DetailView):
    model = RoomModel
    context_object_name = 'room'
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        messages = self.get_object().messagemodel_set.all().order_by('-timestamp')[:100]
        context['messages'] = reversed(messages)
        context['count'] = self.get_object().messagemodel_set.all().count()
        return context


class RoomHistoryView(RoomAuthMixin, LoginRequiredMixin, SingleObjectMixin, ListView):
    paginate_by = 50
    template_name = 'chat/chat_history.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=RoomModel.objects.all())
        return super(RoomHistoryView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.messagemodel_set.all().order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(RoomHistoryView, self).get_context_data(**kwargs)
        context['room'] = self.object
        return context
