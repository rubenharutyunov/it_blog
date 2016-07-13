import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import password_validation
from users.models import User, URLDomainValidator
from users.widgets import FileInputPreview
from users.utils import generate_activation_key, send_activation_email, TOMORROW


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class SignInForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember = forms.BooleanField(required=False)


class SignUpForm(forms.ModelForm):
    email = forms.CharField(max_length=75, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    personal_info = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Personal Info'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        main_fields = ('first_name', 'last_name', 'username',
                       'email', 'password1', 'password2', 'avatar')
        additional_fields = ('personal_info', 'website', 'facebook', 'gplus', 'twitter', 'github', 'linkedin', 'vk')
        fields = main_fields + additional_fields
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
            'facebook': forms.TextInput(attrs={'placeholder': 'Facebook'}),
            'gplus': forms.TextInput(attrs={'placeholder': 'Google Plus'}),
            'twitter': forms.TextInput(attrs={'placeholder': 'Twitter'}),
            'github': forms.TextInput(attrs={'placeholder': 'Github'}),
            'linkedin': forms.TextInput(attrs={'placeholder': 'LinkedIn'}),
            'vk': forms.TextInput(attrs={'placeholder': 'VK'}),
            'avatar': FileInputPreview()
        }

    def main_fields(self):
        return [self[name] for name in filter(lambda x: x in self.Meta.main_fields, self.fields.keys())]

    def additional_fields(self):
        return [self[name] for name in filter(lambda x: x in self.Meta.additional_fields, self.fields.keys())]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match")
        self.instance.username = self.cleaned_data.get('username')
        if password2:
            password_validation.validate_password(password2, self.instance)
        return password2

    def clean_email(self):
        super(SignUpForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.activation_key = generate_activation_key(user.username)  # TODO: Store as hash
        user.key_expires = TOMORROW
        user.save()
        send_activation_email(user.username, user.activation_key, user.email)


class ProfileEditForm(SignUpForm):
    old_password = forms.CharField(widget=forms.PasswordInput())

    class Meta(SignUpForm.Meta):
        SignUpForm.Meta.main_fields = SignUpForm.Meta.main_fields[:4] + \
                                      ('old_password',) + SignUpForm.Meta.main_fields[4:]
        fields = SignUpForm.Meta.fields = SignUpForm.Meta.main_fields + SignUpForm.Meta.additional_fields

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password:
            if not self.instance.check_password(old_password):
                raise forms.ValidationError('Old password is incorrect')
        return old_password

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        user.save()

