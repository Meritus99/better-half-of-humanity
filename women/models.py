from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Women(models.Model):
	title = models.CharField(max_length=255, verbose_name='Title')
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
	content = models.TextField(blank=False, verbose_name='Article text')
	photo = models.ImageField(upload_to='img/', verbose_name='Photo')  # 'photos/%Y/%m/%d'
	time_create = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
	time_update = models.DateTimeField(auto_now=True, verbose_name='Correction time')
	is_published = models.BooleanField(default=True, verbose_name='Publication')
	cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category', related_name='get_posts')
	# related_name = 'get_posts' для того чтоб в shell`e использовать .get_posts.all() а не women_set.all()
	owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE, verbose_name='Author')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post', kwargs={'post_slug': self.slug})

	class Meta:
		verbose_name = 'Famous Women'
		verbose_name_plural = 'Famous Women'
		ordering = ['-time_create']  # "-"(minus)its обратная сортировка


class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True, verbose_name='Name of category')
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category', kwargs={'cat_slug': self.slug})

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'
		ordering = ['id']
