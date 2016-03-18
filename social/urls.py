from django.conf.urls import include, url
from social import views

urlpatterns = [
	url(r'login/', 	views.social_login, name = 'login'),
	url(r'$^',		views.index, name = 'index'	),
	url(r'home/', 	views.home, name = 'home'),
	url(r'stream/', views.stream, name = 'stream'),
	url(r'post/add/', views.add_post, name="add_post"),
	url(r'playlist/add/', views.add_playlist, name="add_playlist"),
	url(r'song/add/', views.add_post, name="add_song"),
	url(r'comment/add/', views.add_comment, name='add_comment'),
	url(r'json/playlist/(?P<playlist_id>[0-9]+)/$', views.get_json_playlist, name='get_json_playlist'),
	url(r'playlist/(?P<playlist_id>[0-9]+)/$', views.get_playlist, name='get_playlist'),
	url(r'playlist/addSong/', views.add_song_to_playlist, name="add_song_to_playlist"),
	url(r'playlist/delete/',   views.delete_playlist, name="delete_playlist"),
]