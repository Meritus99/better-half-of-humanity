from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from transliterate import slugify
from women.models import Category, Women

from .forms import (AddPostForm, ContactForm, EditPageForm, LoginUserForm,
                    RegisterUserForm)
from .utils import DataMixin, content_adjustment, is_owner, menu


class WomenHome(DataMixin, ListView):
    # paginate_by = 5 # pagination, which inclusion in ListView, transmit to utils.py in DataMixin
    model = Women  # эта строчка выбирает все записи из таблицы и пытается их отобразить в виде списка
    template_name = 'women/index.html'  # указываем на какой шаблон должен ссылаться класс представления
    context_object_name = 'posts'

    """ C имени по умолчанию, меняем имя коллекции(object_list) 
    на то, которое удобное для нас,
    и имя переменной можем использовать в указанном шаблоне """

    # extra_context = {'title': 'Главная страница', 'cat_selected': 0}
    """ C пом. этого параметра extra_context можно передавать 
    статические(строки, числа, словари), неизменяемые данные. например списки передавать 
    нельзя(т.к тип данных динамический ).
    если нужно передать динамический контекст, создается след. функция: """

    """ def get_context_data(self, *, object_list=None, **kwargs): # эта функция формирует context для шаблона
            context = super().get_context_data(**kwargs)
            context['menu'] = menu
            context['title'] = 'Главная страница'
            context['cat_selected'] = 0
            return context """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Main page')  # так мы можем задавать параметры нашего контекста
        return context | common_data
        # Вместо варианта сверху, используем DataMixin из utils

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


""" .select_related('cat') чтоб совместно с выборкой постов были загружены данные из таблицы категории
 Так как в модели Women, 'cat' является внешним ключем, который связывает вторичную модель Women
 с первичной Category. Если связь типа ManyToMany, мы бы использовали метод prefetch_related(key)
 Всё это делается для оптимизации сайта, в частности снизить количество напрасных SQL запросов
 В index.html есть строчка {{p.cat}}, благодаря которой, без проделанной выше работы, каждый раз
 происходит обращение к БД, что создает лишнюю нагрузку на СУБД
 .reverse() -- обратный порядок """

""" def index(request):
        posts = Women.objects.filter(is_published=True)
        context = {
            'posts': posts,
            'title': 'Главная страничка',
        }
        return render(request, 'women/index.html', context=context) """


class AboutView(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        # Функция get_context_data формирует контекст для шаблона.
        context = super().get_context_data(**kwargs)
        # get_user_context это метод с класса DataMixin в utils.py
        common_data = self.get_user_context(
            title='Feedback',
            text='Made by Meritus99 ╰‿╯',
            all_women=Women.objects.order_by('-time_update').filter(is_published=True),
            cats=Category.objects.all(),
            cat_selected=None,
        )
        # print(dict(list(context.items()) + list(common_data.items())))
        return context | common_data


# @login_required, для ограничения доступа для неавторизированных юзеров можно использовать данный декоратор
# def about(request):
# 	""" Вариант пагинации для функции представления. Для класса представления это делается мгого проще """
# 	#contact_list = Women.objects.filter(is_published=True)
# 	#paginator = Paginator(contact_list, 5)
# 	#page_number = request.GET.get('page')
# 	#page_obj = paginator.get_page(page_number)
# 	menu = [
# 		{'title': 'О сайте', 'url_name': 'about'},
# 		{'title': 'Добавить статью', 'url_name': 'add_page'},
# 		{'title': 'Обратная связь', 'url_name': 'contact'},
# 	]

# 	cats = Category.objects.annotate(Count('get_posts'))
# 	user_menu = menu.copy()

# 	context = {
# 		'text': 'Made by Meritus99',
# 		'cats': cats,
# 		'menu': user_menu,
# 	}
# 	return render(request, 'women/about.html', context=context) #{'page_obj': page_obj}


def error_handler_404(request, exception):
    content = loader.render_to_string('women/error_404.html', {}, request)
    return HttpResponseNotFound(content)


def error_handler_500(request):
    content = loader.render_to_string('women/error_500.html', {}, request)
    return HttpResponseServerError(content)


class DeletePage(LoginRequiredMixin, DataMixin, DeleteView):
    def get(self, request, post_slug):
        cats = Category.objects.annotate(Count('get_posts'))
        women = Women.objects.get(slug=post_slug)
        cat_selected = women.cat_id
        context = {
            'women': women, 'title': 'Deleting an article', 'menu': menu,
            'cats': cats,
            'cat_selected': cat_selected,
        }

        """ Защита от проникновения """
        html_template = is_owner(request, women)
        if not html_template:
            context['title'] = 'Hahaha'
            context['cat_selected'] = 0
        return render(request, 'women/delete_page.html', context=context)

    def post(self, request, post_slug):
        women = Women.objects.get(slug=post_slug)
        women.delete()
        return redirect('home')


class EditPage(LoginRequiredMixin, DataMixin, UpdateView):
    template_name = 'women/edit_page.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = EditPageForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        check_owner = context["post"]

        """ Защита от проникновения """
        html_template = is_owner(self.request, check_owner)
        if not html_template:
            common_data = self.get_user_context(title='Hahaha', cat_selected=0)
        else:
            common_data = self.get_user_context(title='Editing an article', cat_selected=check_owner.cat_id)

        return context | common_data

    def get_queryset(self):
        """ Усложненный способ защиты от проникновения, но в случае тригера вызывает Http404, что не очень удобно. """
        """ Проверка соответствия имени текущего авторизированого юзера и создателя записи."""

        # women = Women.objects.filter(slug=self.kwargs['post_slug'], is_published=True)
        # if str(self.request.user) != str(women[0].owner.username) and self.request.user.is_superuser == False:
        #    raise Http404

        return Women.objects.filter(slug=self.kwargs['post_slug'], is_published=True)

    def form_valid(self, form):
        form.instance.content = content_adjustment(self.request.POST['content'])
        form.instance.slug = slugify(self.request.POST['title'], 'ru')
        return super().form_valid(form)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):  # кастомный класс
    # класс LoginRequiredMixin - cлужит как ограничение доступа для неавторизированных юзеров
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    # extra_context = {'title': 'Добавление статьи'}

    # women = Women.objects.latest('time_create')	Это бесполезные строки кода, тк ниже я уже писал что
    # редирект по дефолту будет вести на навосозданный пост.
    # redirect = reverse_lazy(f'post/{women.slug}') Поэтому нет смысла вручную выбирать последнюю добавленную статью.

    success_url = reverse_lazy('home')
    """ назначение адреса для редиректа после добавления статьи,
    потому что иначе, класс представления автоматически редиректит по методу get_absolute_url
    прописанному в models """

    """ все переменные ниже, доступны благодаря LoginRequiredMixin """
    # login_url = reverse_lazy('home') # 'login' ссылка редирект для незарегистрированных юзеров
    raise_exception = True  # для того что генерировалась ошибка 403 - доступ запрещен, вместро редирeкта

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Adding an article', cat_selected=None)
        return context | common_data

    def get_initial(self):
        initial = super().get_initial()
        photo = 'img/darken.png'
        initial['photo'] = photo
        return initial

    def form_valid(self, form):
        form.instance.content = content_adjustment(self.request.POST['content'])
        form.instance.owner = self.request.user

        form.instance.slug = slugify(self.request.POST['title'], 'ru')

        return super().form_valid(form)

    # Метод для автозаполнения полей формы
    # def get_initial(self):
    # 	initial = super().get_initial()

    # 	if self.request.method =='POST':
    # 		title = self.request.POST['title']

    # 		initial['slug'] = title
    # 		return initial

    """ если сравнивать с первоначальной функцией addpage, которая находится ниже,
    можно сразу ощутить преимущества классов представления, они позволяют
    писать наш программный код гораздо компактней """


""" def addpage(request):
        if request.method =='POST':
            form = AddPostForm(request.POST, request.FILES) # второй аргумент нужен для успешной передачи 
            # списка файлов который был передан из формы на сервер, для этого обращаемся к коллекции FILES через 
            # объект request
            if form.is_valid():
                # Women.objects.create(**form.cleaned_data) # когда она не связана с моделью, 
                # можно реализовать сохранение в БД подобным образом
                form.save() # когда форма связана с моделью можно воспользоваться методом save
                return redirect('home')
        else:
            form = AddPostForm()
        return render(request, 'women/add_page.html', {'form': form, 'title': 'Добавление статьи'}) """


class NoAccess(DataMixin, TemplateView):
    template_name = 'women/no_access.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Access error')
        return context | common_data


class ContactFormView(DataMixin, FormView):
    # FormView это стандартный базовый класс,
    # для форм которые не привязаны к модели(т.е не работают с БД).

    form_class = ContactForm  # это ссылка на класс ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        # Функция get_context_data формирует контекст для шаблона.
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Feedback', cat_selected=None)
        return context | common_data

    def form_valid(self, form):
        # Вызывается если юзер корректно заполнил все поля формы ContactForm
        with open('feedback.txt', 'a', encoding="utf-8") as f:
            for k, v in form.cleaned_data.items():
                if k == 'captcha':
                    continue
                f.write(str(k) + ': ' + str(v) + "\n")

        return redirect('home')

    """ Метод для автозаполнения полей формы """


# def get_initial(self):
# 	initial = super().get_initial()

# 	email = 'none@email.com'
# 	initial['email'] = email
# 	return initial


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # pk_url_kwarg = # аналогичная механика, если используется pk, a не slug
    slug_url_kwarg = 'post_slug'
    """ по дефолту класс представления берет с юрлов имя слага как 'slug',
    этим параметром slug_url_kwarg, мы указываем нужное нам, корректное название слага """
    context_object_name = 'post'

    # def get_context_data(self, *, object_list=None, **kwargs):
    # 	context = super().get_context_data(**kwargs)
    # 	context['title'] = f'Категория - {context["post"].cat} - {context["post"].title}'
    # 	context['cat_selected'] = context['post'].cat_id
    # 	return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(
            title=f'Category - {context["post"].cat} - {context["post"].title}',
            cat_selected=context['post'].cat_id,
        )
        return context | common_data

    def get_queryset(self):
        return Women.objects.filter(slug=self.kwargs['post_slug'], is_published=True)


""" def show_post(request, post_slug):
        post = get_object_or_404(Women, slug=post_slug, is_published=True)
        context = {
            'post': post,
            'title': post.title,
            'cat_selected': post.cat_id,
        }
        return render(request, 'women/post.html', context=context) """


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # вызывает ошибку 404 если коллекция(список) пустая

    # def get_context_data(self, *, object_list=None, **kwargs):
    # 	context = super().get_context_data(**kwargs)
    # 	context['title'] = f'Категория - {context["posts"][0].cat}'
    # 	""" берем первый элемент коллекции posts и обращаемся к атрибуту cat чтобы узнать
    # 	название категории """
    # 	context['cat_selected'] = context['posts'][0].cat_id
    # 	""" тоже самое но обращаемся к идентификатору выбранной категории """
    # 	return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['cat_slug'])
        common_data = self.get_user_context(
            title=f'Category - {category.name}',
            cat_selected=category.pk,
        )
        return context | common_data

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    """ через словарь kwargs можем получить все параметры нашего маршрута(который описан в юрлах) """


# def show_category(request, cat_slug):
# 	cat = Category.objects.get(slug = cat_slug)
# 	posts = Women.objects.filter(cat_id=cat, is_published=True)
#
# 	if len(posts) == 0:
# 		raise Http404()
#
# 	context = {
# 		'posts': posts,
# 		'title': 'Отображение по рубрикам',
# 		'cat_selected': cat.id,
# 	}
#
# 	return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title="Registration", cat_selected=None)
        return context | common_data

    def form_valid(self, form):  # этот метод вызывается при успешной проверке формы регистрации
        user = form.save()  # здесь мы ручками сохраняем форму в БД, т.е добавляем юзера в БД
        login(self.request, user)  # здесь вызываем функцию фреймворка джанго, которая авторизовывает пользователя
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Authorization', cat_selected=None)
        return context | common_data

    def get_success_url(self):
        # чтобы после авторизации был редирект на главную, можно в файле settings.py прописать LOGIN_REDIRECT_URL = '/'
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
