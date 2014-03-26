from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='')
    password = forms.CharField(widget=forms.PasswordInput, label='')
    remember = forms.BooleanField(required=False, label='Remember me')

    error_messages = {
        'invalid_login': _("Please enter a correct username and password"),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', placeholder='Email or username'),
            Field('password', placeholder='Password'),
            Field('remember', css_class='', template='bootstrap3/field.html'),
        )
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-success btn-lg btn-block'))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(email__iexact=username)
                username = user.username
            except User.DoesNotExist:
                pass
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
        
        