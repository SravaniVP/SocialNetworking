from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# models.py
class Status(models.Model):
    owner = models.ForeignKey(User,on_delete = models.CASCADE,)
    description = models.TextField()
    status_Img = models.ImageField(upload_to = 'images/')
    likes = models.ManyToManyField(User,related_name='likes',blank=True)

    def get_absolute_url(self):
        return reverse('detail_status',args=[self.id])

    def total_likes(self):
        return self.likes.count()

    def total_status(self):
        return self.status_Img.count()

class Comment(models.Model):
    status = models.ForeignKey(Status,on_delete = models.CASCADE,)
    user = models.ForeignKey(User,on_delete = models.CASCADE,)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.status.id,str(self.user.username))



