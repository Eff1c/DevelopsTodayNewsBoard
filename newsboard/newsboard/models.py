from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    creation_date = models.DateField(auto_now_add=True)
    amount_of_upvotes = models.IntegerField(default=0)
    author_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["-amount_of_upvotes"]

class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments",)

    class Meta:
        ordering = ["-creation_date"]
