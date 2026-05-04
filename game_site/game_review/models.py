from django.conf import settings
from django.db import models

# Create your models here.
class GameReview(models.Model):
    title = models.CharField(max_length=250)
    reviewer = models.CharField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='game_reviews', null=True, blank=True)
    rating = models.IntegerField()
    review_text = models.TextField()
    submission = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ReviewLike",
        related_name="review_likes"
    )

    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"{self.title} | {self.reviewer} | {self.rating}"

    @property
    def user_has_liked(self):
        return self.likes.filter(user=self.current_user).exists()

#Create user profile model
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%y/%m/%d',
        blank=True
    )
    def __str__(self):
        return f'Profile of {self.user.username}'
    
class ReviewLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= "liked_reviews",
        on_delete = models.CASCADE
    )
    review = models.ForeignKey(
        GameReview,
        related_name= "likes",
        on_delete = models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"{self.user} liked {self.review}"
    

# Game genres for review
class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'game'
        verbose_name_plural = 'games'
    def __str__(self):
        return self.name
class Genre(models.Model):
    game = models.ForeignKey(
        Game,
        related_name='genre',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(
        upload_to='genre/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]
    def __str__(self):
        return self.name