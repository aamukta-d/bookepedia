from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=128, blank=True, unique=True)
    author = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=2000, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) 
    cover = models.ImageField(upload_to='book_covers', blank = True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) 
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return self.title
    
class UserBookInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True,blank=True)
    liked = models.BooleanField(default=False)

def get_books_by_user_genre(user, limit=3):
    preferred_genres = user.userprofile.top_genre.all()
    recommended_books = Book.objects.filter(genre__in=preferred_genres).distinct()[:limit]
    return recommended_books

class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    top_genre = models.ManyToManyField(Genre)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
    def get_following(self):
        return User.objects.filter(following__follower=self.user)
    
    def get_followers(self):
        return User.objects.filter(followers__followed=self.user)

class UserFollowing(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_followers')
        ]
        ordering = ['-created']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"