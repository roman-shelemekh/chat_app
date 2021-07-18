from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
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
                return HttpResponseRedirect(reverse('chat:room', args=[room.room_name]))
            else:
                self.create_form.validation_error_class()
        elif request.POST.get('button') == 'enter':
            self.enter_form = RoomEnterForm(request.POST)
            if self.enter_form.is_valid():
                room_name = self.enter_form.cleaned_data.get('room_name')
                return HttpResponseRedirect(reverse('chat:room', args=[room_name]))
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


@login_required
def room(request, room_name):
    return render(request, 'chat/chat.html', {'room_name': room_name})
