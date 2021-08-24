from django.db import models
from django.contrib.auth.models import User


class MajorPost(models.Model):
    major = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.BooleanField()

    title = models.CharField(max_length=100)
    contents = models.TextField()
    image = models.ImageField(blank=True, upload_to="major/image")
    file = models.FileField(blank=True, upload_to="major/file")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def click(self):  # 조회수
        self.hits += 1
        self.save()