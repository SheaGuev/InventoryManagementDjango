from django import forms
from django.contrib.auth.forms import UserCreationForm
from InventoryManagement.models import CustomUser

class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={'required': ''},
        help_text='',
    )
    first_name = forms.CharField(
        required=True,
        error_messages={'required': ''},
        help_text='',
    )
    last_name = forms.CharField(
        required=True,
        error_messages={'required': ''},
        help_text='',
    )
    phone = forms.CharField(
        required=True,
        error_messages={'required': ''},
        help_text='',
    )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput,
    #     error_messages={'required': ''},
    #     help_text='',
    # )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': ''},
        help_text='',
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)