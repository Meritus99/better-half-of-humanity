from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Women


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'time_create', 'preview', 'is_published', 'owner')
	list_display_links = ('id', 'title')  # for clickable fields
	search_fields = ('title', 'content')
	list_editable = ('is_published',)
	list_filter = ('is_published', 'time_create')
	prepopulated_fields = {'slug': ('title',)}  # automatic filling of the slug field based on the title field
	
	fields = ('title', 'slug', 'cat', 'content', 'photo', 'preview', 'owner', 'is_published', 'time_create', 'time_update')
	# the fields attribute contains the order and list of editable fields that should be displayed in the edit form.
	readonly_fields = ('time_create', 'time_update', 'preview', 'owner')

	def preview(self, obj):
		if obj.photo:
			return mark_safe(f'<img src="{obj.photo.url}" width=90>')
	preview.short_description = 'Миниатюра'  # if we want to change the label


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}
# Without using the decorator, the models can be registered as follows:
# admin.site.register(Women, WomenAdmin)
# admin.site.register(Category, CategoryAdmin)


""" The attributes for the admin panel can be changed in this way. These 
parameters are used in the html templates, in particular in the custom template base_site.html 
(file is located in 'templates/admin'), which we re-purposed from the standard """

admin.site.site_title = "Women's website admin panel"
admin.site.site_header = "Women's website admin panel 2"
