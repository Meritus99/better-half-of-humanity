from django.core.cache import cache
from django.db.models import Count

from .models import Category

menu = [
    {'title': 'About the site', 'url_name': 'about'},
    {'title': 'Add article', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
]


def content_adjustment(string):
    numbers = [x for x in range(0, 101)]
    for number in numbers:
        string = string.replace(f'[{str(number)}]', '')
    return string


def is_owner(request, self):
    if self.owner == request.user:
        return True
    return False


class DataMixin:
    paginate_by = 5  # pagination, which inclusion in ListView

    def get_user_context(self, **kwargs):
        context = kwargs
        """ Low level API caching/Can be used
        to put some individual data in the cache, 
        and then read them out: """

        cats = cache.get('cats')  # ('cats') - имя ключа
        if not cats:
            cats = Category.objects.all().annotate(Count('get_posts'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
