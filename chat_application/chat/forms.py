from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import RoomModel


class ErrorClassMixin:
    def validation_error_class(self):
        for field in self:
            if field.errors:
                field.field.widget.attrs['class'] += ' is-invalid'
        if self.non_field_errors():
            for field in self:
                field.field.widget.attrs['class'] += ' is-invalid'


class RoomEnterForm(ErrorClassMixin, forms.Form):
    room_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название комнаты'}),
        label='Название комнаты')
    room_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль для входа в комнату'}),
        label='Пароль для входа')

    def clean(self):
        if self.cleaned_data.get('room_name') and self.cleaned_data.get('room_password'):
            try:
                room = RoomModel.objects.get(room_name=self.cleaned_data['room_name'])
            except:
                raise forms.ValidationError('Комнаты c таким названием не существует.')
            submitted_password = self.cleaned_data['room_password']
            if not check_password(submitted_password, room.room_password):
                raise forms.ValidationError('Неверный пароль.')
        return self.cleaned_data


class RoomCreateForm(ErrorClassMixin, forms.Form):
    room_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название комнаты'}),
        label='Название комнаты')
    room_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль для входа в комнату'}),
        label='Пароль для входа')
    room_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        label='Повторите пароль')

    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        try:
            room = RoomModel.objects.get(room_name=room_name)
        except RoomModel.DoesNotExist:
            return room_name
        else:
            raise forms.ValidationError('Комната с таким названием уже существует.')


class SignUpForm(ErrorClassMixin, UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Имя'}),
        }


class LoginForm(ErrorClassMixin, AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя', 'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
