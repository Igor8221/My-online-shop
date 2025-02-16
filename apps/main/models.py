from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager 


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news_images/')
    tags = TaggableManager()
    text = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title