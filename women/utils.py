from django.db.models import Count
from django.core.cache import cache
from .models import *


menu = [
	{'title': 'About the site', 'url_name': 'about'},
	{'title': 'Add article', 'url_name': 'add_page'},
	{'title': 'Feedback', 'url_name': 'contact'},
]

class DataMixin:
	paginate_by = 5 # pagination, which inclusion in ListView

	def get_user_context(self, **kwargs):
		context = kwargs
		""" Кэширование с использованием API низкого уровня/Может быть использовано
		для того чтобы помещать в кэш какие-то отдельные данные, 
		а потом их читать: """
		cats = cache.get('cats') # ('cats') - имя ключа
		if not cats:
			cats = Category.objects.all().annotate(Count('get_posts'))
			cache.set('cats', cats, 60)

		women = Women.objects.all()
		user_menu = menu.copy()
		if not self.request.user.is_authenticated:
			user_menu.pop(1)

		context['menu'] = user_menu
		context['cats'] = cats
		if 'cat_selected' not in context:
			context['cat_selected'] = 0
		return context
