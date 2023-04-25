from captcha.fields import CaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from women.models import Women
from women.validators import validate_content, validate_title


class AddPostForm(forms.ModelForm):
	captcha = CaptchaField(label='Enter a code', required=settings.REQUIRED_CAPTCHA)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["title"].validators = [validate_title]  # you can implement validators from another file
		self.fields["content"].validators = [validate_content]
		# self.fields['photo'].required = self.flag
		self.fields["cat"].empty_label = "Category not selected"

	class Meta:
		model = Women
		fields = ['title', 'content', 'photo', 'is_published', 'cat']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'input', 'placeholder': ' Name Surname'}),
			# a class from our css to set the field style
			'content': forms.Textarea(attrs={'class': 'textarea', 'cols': 60, 'rows': 8}),
		}


class RegisterUserForm(UserCreationForm):
	username = forms.CharField(
		label="Login", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': ' login'}))
	email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(
		attrs={'class': 'form-input', 'placeholder': ' example@email.com'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	password2 = forms.CharField(label='Repeat pass', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	captcha = CaptchaField(label='Enter a code', required=settings.REQUIRED_CAPTCHA)

	class Meta:
		# fields have the same order as they are written in the fields variable
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'captcha')


class LoginUserForm(AuthenticationForm):
	username = forms.CharField(label='Login', widget=forms.TextInput(
		attrs={'class': 'form-input', 'placeholder': ' username'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(
		attrs={'class': 'form-input', 'placeholder': ' password'}))


class ContactForm(forms.Form):
	name = forms.CharField(label='Name', max_length=255, widget=forms.TextInput(
		attrs={'class': 'form-input', 'placeholder': 'Your name'}))
	email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(
		attrs={'class': 'form-input', 'placeholder': 'example@gmail.com'}))
	content = forms.CharField(label="Message", widget=forms.Textarea(attrs={'cols': 46, 'rows': 3}))
	captcha = CaptchaField(label='Enter a code', required=settings.REQUIRED_CAPTCHA)


class EditPageForm(forms.ModelForm):
	captcha = CaptchaField(label='Enter a code', required=settings.REQUIRED_CAPTCHA)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["title"].validators = [validate_title]
		self.fields["content"].validators = [validate_content]

	class Meta:
		model = Women
		fields = ['title', 'content', 'photo', 'cat']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-input'}),
			'content': forms.Textarea(attrs={'cols': 60, 'rows': 8}),
		}
