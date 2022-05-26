from django.contrib.auth.models import User
from django.db import models

LANGS = [
    ("py", "python"),
    ("js", "JavaScript"),
    ("cpp", "C++")]


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, related_name="snippets")


class Comment(models.Model):
    text = models.TextField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name='comments')
