from django.db import models
from django.contrib.auth.models import User
from mutagen.mp3 import MP3 

# Create your models here.

class Post(models.Model):
	text = models.TextField()
	poster = models.ForeignKey(User)
	date_time = models.DateTimeField(auto_now=True)
	photo = models.ImageField(null = True, blank=True)

class Comment(models.Model):
	text = models.TextField()
	poster = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	date_time = models.DateTimeField(auto_now = True)
	class Meta:
		ordering = ['-date_time']

		
		
		
		
class Genre(models.Model):
	name = models.CharField(max_length = 50)
	def __str__(self):
		return self.name
		
		


class Artist(models.Model):
	name = models.TextField()
	profilePicture = models.ImageField()
	def __str__(self):
		return self.name
	
class Album(models.Model):
	name = models.CharField(max_length = 50)
	savedBy = models.ManyToManyField(User)
	artist 	= models.ForeignKey(Artist)
	genre 	= models.ManyToManyField(Genre)
	profilePicture = models.ImageField()
	lastPlayed = models.DateTimeField(auto_now = True)
	def __str__(self):
		return self.name

			

	
class Song(models.Model):
	name	= models.CharField(max_length = 50)
	artist	= models.ForeignKey(Artist)
	genre 	= models.ManyToManyField(Genre)
	album	= models.ForeignKey(Album)
	audioFile = models.FileField(upload_to="musicDatabase/")
	lastPlayed = models.DateTimeField()
	songLength = models.FloatField()
	def __str__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		song = MP3(self.audioFile)
		self.songLength = song.info.length
		super(Model, self).save(*args, **kwargs)
	  

class Playlist(models.Model):
	name = models.CharField(max_length = 50)
	owner = models.ForeignKey('auth.User')
	savedBy = models.ManyToManyField(User, related_name='savedBy')
	songs = models.ManyToManyField(Song)
	lastPlayed = models.DateTimeField(auto_now = True)
	cover  = models.ImageField(default='/media/1.jpg')
	def __str__(self):
		return self.name	
	


class UserProfile(models.Model):
	user = models.ForeignKey(User)
	playlists = models.ManyToManyField(Playlist)
	friends = models.ManyToManyField(User, related_name = 'UserProfile')
	albums = models.ManyToManyField(Album)
	allSongs = models.ManyToManyField(Song)
	profilePicture = models.ImageField()
	def __str__(self):
		return self.name
