from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class WomenAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'time_create', 'preview', 'is_published', 'owner') # для отображения доп. полей в админке
	list_display_links = ('id', 'title') #для полей на которые можно кликнуть
	search_fields = ('title', 'content')
	list_editable = ('is_published',)
	list_filter = ('is_published', 'time_create')
	prepopulated_fields = {'slug': ('title',)} # автоматическое заполнение поля слаг на основе поля title
	
	fields = ('title', 'slug', 'cat', 'content', 'photo', 'preview', 'owner', 'is_published', 'time_create', 'time_update')
	# атрибут fields содержит порядок и список редактируемых полей, которые стоит отображать в форме редактирования.
	readonly_fields = ('time_create', 'time_update', 'preview', 'owner') # нередактируемые поля, только для чтения.


	def preview(self, obj):
		# Функция mark_safe, указывает не экранировать теги (img и тд), т.е будут выполняться
		# благодаря фильтру safe, который добавляется к фрагменту html кода 
		if obj.photo:
			return mark_safe(f'<img src="{obj.photo.url}" width=90>')

	preview.short_description = 'Миниатюра' # if we wanna change the label


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля слаг на основе поля name

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

""" Таким способом можно изменять атрибуты для админ.панели(полный список смотреть в документации). Эти параметры используются в html шаблонах, в частности в кастомном шаблоне base_site.html (который лежит в 'templates/admin'), который мы переопеределили от стандартного"""
admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = "Админ-панель сайта о женщинах 2"
