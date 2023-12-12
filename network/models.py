from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass




class Post(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user} added a post at {self.datetime}'


class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following_user')
    user_follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_follower')

    def __str__(self):
        return f'{self.user} is following {self.user_follower} '
    

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='liking_user')
    post_liked = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_liked')

    def __str__(self):
        return f'{self.user} liked {self.post_liked} '
