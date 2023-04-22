from captcha.fields import CaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from women.models import Women
from women.validators import validate_content, validate_title

""" class AddPostForm(forms.Form):
		title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Заголовок')
		slug = forms.SlugField(max_length=255, label='URL')
		content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label="Содержимое")
		is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
		# атрибут required=False --> делает это поле необязательным, 
		# а initial=True будет делать поле подефолту отмеченым
		cat = forms.ModelChoiceField(
			queryset=Category.objects.all(),
			label="Категория",
			empty_label='Категория не выбрана'), """


class AddPostForm(forms.ModelForm):
	captcha = CaptchaField(label='Enter a code', required=settings.REQUIRED_CAPTCHA)
	""" функция ниже для того чтоб внести дополнительные настройки отображения """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["title"].validators = [validate_title]  # так можно внедрить валидаторы из отдельного файла
		self.fields["content"].validators = [validate_content]
		# self.fields['photo'].required = self.flag
		self.fields["cat"].empty_label = "Category not selected"

	class Meta:
		model = Women
		fields = ['title', 'content', 'photo', 'is_published', 'cat']  # можно '__all__',
		# но рекомендуется явно указывать нужные поля как сделано выше

		widgets = {
			'title': forms.TextInput(attrs={'class': 'input', 'placeholder': ' Name Surname'}),
			# класс из нашего цсс для установления стиля поля
			'content': forms.Textarea(attrs={'class': 'textarea', 'cols': 60, 'rows': 8}),  # 60 колонок и 10 строчек
		}

		""" Пользовательский валидатор для создания пользовательских валидаторов, в форме нужно прописать метод
		с именем описываемого поля.(clean_'name_of_field') В своей работе 
		метод должен генерировать исключение ValidationError """


class RegisterUserForm(
	UserCreationForm):  # расширяем джанговский класс UserCreationForm(он является стандартным от джанго)
	username = forms.CharField(
		label="Login", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': ' login'}))
	email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(
		attrs={'class': 'form-input', 'placeholder': ' example@email.com'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	password2 = forms.CharField(label='Repeat pass', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	captcha = CaptchaField(label='Enter a code')

	# def __init__(self, *args, **kwargs): Не нужная часть кода, тк мы уже определили нужные нам поля выше
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['username'].label = "Логин"

	class Meta:
		""" хз зачем оно если есть верхние настройки, но выяснил что выстраивает поля как указано в fields """
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
	captcha = CaptchaField(label='Enter a code')


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
			'title': forms.TextInput(attrs={'class': 'form-input'}),  # класс из нашего цсс для установления стиля поля
			'content': forms.Textarea(attrs={'cols': 60, 'rows': 8}),  # 60 колонок и 10 строчек
		}
