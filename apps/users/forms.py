from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        if not email and not phone_number:
            raise forms.ValidationError("Необходимо заполнить либо email, либо номер телефона.")
        return cleaned_data


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("Старый пароль введен неверно.")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Новые пароли не совпадают.")
        password_validation.validate_password(new_password2, self.user)
        return new_password2

    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()

class ChangePhoneForm(forms.ModelForm):
    phone_number = forms.CharField(
        label="Новый номер телефона",
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|7|8)?[9]\d{9}$',
                message="Введите корректный российский номер телефона."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['phone_number']