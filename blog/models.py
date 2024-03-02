from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    intro = models.TextField()
    body = models.TextField()
    image1 = models.ImageField(upload_to='images/', blank=True)
    image2 = models.ImageField(upload_to='images/', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']#<---- Ordering from newest to oldest

    def save(self, *args, **kwargs):#<----- making the title the unique identifier for querying the db table
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    #Deleting Post
    def delete_post(self):
        self.delete()

    def __str__(self):
        return self.title 