from django import template
from women.models import Category

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
	if not filter:
		return Category.objects.all()
	else:
		return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
	if not sort:
		cats = Category.objects.all()
	else:
		cats = Category.objects.order_by(sort)

	return {'cats': cats, 'cat_selected': cat_selected}
# The returned dictionary will automatically be passed to the pattern,
# that we defined above


@register.inclusion_tag('women/list_menu.html')
def show_menu():
	menu = [
		{'title': 'About the site', 'url_name': 'about'},
		{'title': 'Add article', 'url_name': 'add_page'},
		{'title': 'Feedback', 'url_name': 'contact'},
	]
	return {'menu': menu}
