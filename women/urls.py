from women.views import *
from django.urls import path, re_path
from django.views.decorators.cache import cache_page

'''	Кэширование на уровне представлений. Любое кэширование применяется только 
	нa финальном этапе разработки, чтобы не скрывать от разрабротчика реальную 
	нагрузку на сайт. '''

urlpatterns = [

#	path('', cache_page(60)(WomenHome.as_view()), name='home'), 
	# в папке coolsite_cache создаются бинарные файлы, которые сохраняют кэш главной страницы, 
	# в итоге при повторном обращении к странице не происходит(SQL запроса) обращения к БД, 
	# потому что данные берутся из кэша, что существенно снижает нагрузку на сайт.

	# по истечении времени(60 сек.), этот кэш перестанет существовать, и очередной запрос снова будет формировать нашу страницу
	# Нюанс, пока существует этот кэш, любые изменения страницы не будут отображаться юзеру, 
	# т.к будет брать ранее сформированную страницу из кэша.
	# Это означает что динамические данные(чаты, комментарии) кэшировать нельзя

	path('', WomenHome.as_view(), name='home'), 
	path('post/<slug:post_slug>/delete/', DeletePage.as_view(), name='delete_page'),
	path('post/<slug:post_slug>/edit/', EditPage.as_view(), name='edit_page'),
	path('post/<slug:post_slug>/access-error/', NoAccess.as_view(), name='no_access'),
	path('about/', AboutView.as_view(), name='about'),
	path('addpage/', AddPage.as_view(), name='add_page'),
	path('contact/', ContactFormView.as_view(), name='contact'),
	path('login/', LoginUser.as_view(), name='login'),
	path('logout/', logout_user, name='logout'),
	path('register/', RegisterUser.as_view(), name='register'),
	path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
	path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),

	
]
