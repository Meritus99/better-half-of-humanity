from django.urls import path
from .views import *

"""	Caching at view level. Any caching is only applied in the 
	at the final design stage, so as not to hide the actual 
	load on the site. """

""" path('', cache_page(60)(WomenHome.as_view()), name='home''), 
binary files are created in the coolsite_cache folder, which saves the main page cache, 
as a result, when the page is accessed again, there is no (SQL request) to the database, 
because data is taken from the cache, which significantly reduces the load on the site. """

""" After 60 seconds, this cache will cease to exist, 
and the next request will build our page again.
The nuance, while there is this cache, any changes of page will not be displayed to the user, 
because it will take a previously generated page from the cache.
This means that dynamic data (chats, comments) cannot be cached. """

urlpatterns = [
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
