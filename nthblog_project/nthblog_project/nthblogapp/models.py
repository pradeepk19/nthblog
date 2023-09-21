from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    author = models.ForeignKey(User, related_name='blog_post', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    likes =  models.ManyToManyField(User, related_name='likes', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    restrict_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.id, self.slug])

    def total_likes(self):
        return self.likes.count()

@receiver(pre_save, sender = Post)
def pre_save_slug(sender, **kwargs):
    slug123 = slugify(kwargs['instance'].title)  #its first post  ---> its-first-post
    kwargs['instance'].slug = slug123


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    phote = models.ImageField(null=True, blank=True, upload_to='images')



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    reply = models.ForeignKey('Comment', null=True, related_name='replies',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.user.username)








