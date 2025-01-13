from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author= models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)  
    email = models.EmailField()  # do not delete this
    content = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    status = models.BooleanField(default=True)  # If the comment is published or not

    class Meta:
        ordering = ("publish",)

    def __str__(self):
        return f"Comment by {self.user.username}"
