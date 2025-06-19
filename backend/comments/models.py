from django.db import models
from django.core.validators import RegexValidator, URLValidator

from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=120)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True, validators=[URLValidator()])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.email})'


class CommentAttachment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    name = models.CharField(max_length=255)
