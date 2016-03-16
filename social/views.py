from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from social.models import Post
from social.models import Comment, Post # put this at the top with the other imports
from social.models import Playlist, Artist, Album, Song, UserProfile


# Create your views here.

def index(request):
	return render(request, 'social/index.html')
	
def social_login(request):
   check = _check_post_request(request, ['username', 'password'])
   if check[0]:
       user = authenticate(username=request.POST['username'], password=request.POST['password']) 
       if user is not None:
           login(request, user)
           return HttpResponseRedirect(reverse('social:stream'))
       else:
           return HttpResponseBadRequest("The combination of username and password does not exist.")
   else:
       return HttpResponseBadRequest(check[1])
		
@login_required
def stream(request):
	if request.method == 'GET':
		userPlaylists = Playlist.objects.filter(owner=request.user)
		user = UserProfile.objects.filter(user=request.user)
		print("bla")
	elif request.method == 'POST':
		check = _check_post_request(request, ['search_terms'])
		if check[0]:
			search_term = request.POST['search_terms']
			playlists = Playlist.objects.filter(text__icontains=search_term, user=request.user)
			songs = Song.objects.filter(text__icontains=search_term)
		else:
			return HttpResponseBadRequest(check[1])
	return render(request, 'social/stream.html', {'userPlaylists': userPlaylists, 'user':user})


	
@login_required
def add_song_to_playlist(request):
	
	check = _check_post_request(request, ['text'])
	if check[0]:
		new_song = Song()
		new_song.name = request.POST['text']
		new_song.artist = request.username
		new_song.save()
		return HttpResponseRedirect(reverse('social:stream'))
	else:
		return HttpResponseBadRequest(check[1]);	

@login_required		
def add_playlist(request):
	check = _check_post_request(request, ['text'])
	if check[0]:
		new_playlist = Playlist()
		new_playlist.name = request.POST['text']
		new_playlist.owner = request.username
		new_playlist.save()
		return HttpResponseRedirect(reverse('social:stream'))
	else:
		return HttpResponseBadRequest(check[1]);
	
@login_required
def home(request):
    if request.method == 'GET':
        posts = Post.objects.all()
    elif request.method == 'POST':
        check = _check_post_request(request, ['search_terms'])
        if check[0]:
            search_term = request.POST['search_terms']
            posts = Post.objects.filter(text__icontains=search_term)
        else:
            return HttpResponseBadRequest(check[1])
    posts = posts.order_by('-date_time')
    return render(request, 'social/home.html', {'posts': posts})

@login_required
def add_post(request):
	
	check = _check_post_request(request, ['text'])
	if check[0]:
		new_post = Post()
		new_post.text = request.POST['text']
		new_post.poster = request.user
		if 'photo' in request.FILES and request.FILES['photo'] is not None:
			new_post.photo = request.FILES['photo']
		new_post.save()
		return HttpResponseRedirect(reverse('social:home'))
	else:
		return HttpResponseBadRequest(check[1]);

@login_required		
def add_comment(request):
	check = _check_post_request(request, ['comment'])
	if check[0]:
		new_comment = Comment()
		new_comment.text = request.POST['comment']
		new_comment.poster = request.user
		try:
			post = Post.objects.get(pk=request.POST['post_id'])
			new_comment.post = post
		except Post.DoesNotExist:
			return HttpResponseBadRequest("There is no Post with id {}".format(request.POST['post_id']))
		new_comment.save()
		return HttpResponseRedirect(reverse('social:home'))
	else:
		return HttpResponseBadRequest("check[1]")
		
def _check_post_request(request, keys):
	#check if request method is POST
	if request.method != 'POST':
		return (False, "This method shuld be called with a POST method")
	for key in keys:
		# Check that the key exists
		if key not in request.POST:
			return (False, "The POST request should contain a {} field". format(key))
		# Check that the text is not empty
		if not request.POST[key]:
			return(False, "The {} field cannot be empty!".format(key))
	
	return (True, "Everything is fine")
	
def get_playlist(request, playlist_id):
	playlist = Playlist.objects.get(pk=playlist_id)
	return render(request, 'social/playlist.html', {'playlist': playlist})

def get_json_playlist(request, playlist_id):
	playlist = Playlist.objects.get(pk=playlist_id)
	result = {}
	result['name'] = playlist.name
	result['id'] = playlist.id
	result['coverUrl'] = playlist.cover.url
	result['savedBy'] = []
	for user in playlist.savedBy.all():
		user_obj = {}
		user_obj['id'] = user.id
		user_obj['name'] = user.username
		
	result['songs'] = []
	for song in playlist.songs.all():
	  song_obj = {}
	  song_obj['id'] = song.id
	  song_obj['name'] = song.name
	  song_obj['artist'] = {'name': song.artist.name, 'id': song.artist.id}
	  song_obj['url'] = song.audioFile.url
	  song_obj['album'] = {'name': song.album.name, 'id': song.album.id}
	  result['songs'].append(song_obj)
	return HttpResponse(json.dumps(result))


	

	
