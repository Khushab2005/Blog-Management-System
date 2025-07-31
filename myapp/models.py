from django.db import models
import os
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50,blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

        
    def __str__(self):
        return self.username
    


def upload_path(instance, filename):
    name = instance.author.username.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name}.{ext}" 
    return os.path.join("blog_images", name, new_filename)


class Blog(models.Model):
    images = models.ImageField(upload_to=upload_path, blank=True, null=True)
    title = models.CharField(max_length=100 , blank=False,null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
     
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.author} on {self.blog}"
    
    
    
            