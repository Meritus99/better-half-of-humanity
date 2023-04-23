import requests

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.base import ContentFile
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from transliterate import slugify
from .models import Category, Women

from .forms import (AddPostForm, ContactForm, EditPageForm, LoginUserForm,
                    RegisterUserForm)
from .utils import DataMixin, content_adjustment, is_owner, initial_photo, menu


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Main page')
        return context | common_data

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


class AboutView(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # get_user_context - method from the DataMixin class in utils.py
        common_data = self.get_user_context(
            title='Feedback',
            text='Made by Meritus99 ╰‿╯',
            all_women=Women.objects.order_by('-time_update').filter(is_published=True),
            cats=Category.objects.all(),
            cat_selected=None,
        )
        # return(dict(list(context.items()) + list(common_data.items())))
        return context | common_data


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
        return Women.objects.filter(slug=self.kwargs['post_slug'], is_published=True)

    def form_valid(self, form):
        form.instance.content = content_adjustment(self.request.POST['content'])
        form.instance.slug = slugify(self.request.POST['title'], 'ru')
        return super().form_valid(form)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    raise_exception = True  # to generate a 403 error - access denied, instead of a redirect

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Adding an article', cat_selected=None)
        return context | common_data

    def get_initial(self):
        initial = super().get_initial()
        response = requests.get(initial_photo)
        image_content = response.content
        file_name = initial_photo.split('/')[-1]
        initial['photo'] = ContentFile(image_content, name=file_name)
        return initial

    def form_valid(self, form):
        form.instance.content = content_adjustment(self.request.POST['content'])
        form.instance.owner = self.request.user
        form.instance.slug = slugify(self.request.POST['title'], 'ru')
        return super().form_valid(form)


class NoAccess(DataMixin, TemplateView):
    template_name = 'women/no_access.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Access error')
        return context | common_data


class ContactFormView(DataMixin, FormView):
    # FormView standard class for forms that are not linked to a model (do not work with the database).
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        # The get_context_data function generates the context for the template.
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Feedback', cat_selected=None)
        return context | common_data

    def form_valid(self, form):
        # Called if the user has filled in all fields of the ContactForm correctly
        with open('feedback.txt', 'a', encoding="utf-8") as f:
            for key, value in form.cleaned_data.items():
                if key == 'captcha':
                    continue
                f.write(str(key) + ': ' + str(value) + "\n")

        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'
    # pk_url_kwarg = # similar mechanics if using a pk rather than a slug
    slug_url_kwarg = 'post_slug'
    # By default, the view class takes the name of the slug as 'slug',
    # with this parameter slug_url_kwarg, we specify the correct name of the slug

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(
            title=f'Category - {context["post"].cat} - {context["post"].title}',
            cat_selected=context['post'].cat_id,
        )
        return context | common_data

    def get_queryset(self):
        return Women.objects.filter(slug=self.kwargs['post_slug'], is_published=True)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # invoke a 404 error if the collection(list) is empty

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
    # via the kwargs dictionary I can get all the parameters of our route (which is described in the urls)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title="Registration", cat_selected=None)
        return context | common_data

    def form_valid(self, form):
        user = form.save()  # here we save the form in the database, i.e. we add the user to the database
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        common_data = self.get_user_context(title='Authorization', cat_selected=None)
        return context | common_data

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def error_handler_404(request, exception):
    content = loader.render_to_string('women/error_404.html', {}, request)
    return HttpResponseNotFound(content)


def error_handler_500(request):
    content = loader.render_to_string('women/error_500.html', {}, request)
    return HttpResponseServerError(content)
