from django.db import models
from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comm_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        post_comm_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']


        print(posts_rating)
        print('--------')
        print(comm_rating)
        print('--------')
        print(post_comm_rating)

        self.rating = posts_rating * 3 + comm_rating + post_comm_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)



class Post(models.Model):
    news = 'NS'
    article = 'AR'

    POSITIONS = [
        (news, "новость"),
        (article, "Статья")
    ]
    positions = models.CharField(max_length=2, choices=POSITIONS, default=news)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)



    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    comm_text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

