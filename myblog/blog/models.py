

# # Create your models here.
from django.db import models
from django.contrib.auth.models import User

# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

#     def __str__(self):
#         return self.title

# class Comment(models.Model):
#     blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Comment by {self.author} on {self.blog}'
#model.py
from django.db import models
class BlogQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    # user = models.ForeignKey( User, on_delete=models.CASCADE, related_name = "blogs" ) #changed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted=models.BooleanField(default=False)
    objects=BlogQuerySet.as_manager()
    
    def delete(self, using = None, keep_parents = False):
        self.is_deleted=True
        self.save()
    def restore(self):
        self.is_deleted=False
        self.save()

    def __str__(self):
        return self.title

from django.db import models

class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments'  
    )
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'  
    )
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author_name} - {self.content[:30]}" # author's name and the first 30 characters of the comment's content.

    