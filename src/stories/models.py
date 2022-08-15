from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from PIL import Image, ExifTags
import pytz
import io
import os
from django.core.files import File


class Category(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()

    def __str__(self):
        return self.name


class Issue(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Story(models.Model):
    title = models.CharField(max_length=100)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    content_text = models.TextField(verbose_name='your Text')

    issue_to_write_about = models.ForeignKey(
        Issue, on_delete=models.SET_NULL, default=1, verbose_name='Topic to write about', null=True)

    category_to_write_about = models.ForeignKey(
        Category, on_delete=models.SET_NULL, default=1, null=True)
    picture = models.ImageField(
        upload_to='story_imgs', blank=True, verbose_name='Optional Picture')
    picture_caption = models.CharField(
        max_length=200, blank=True, verbose_name='Optional Caption for Picture')

    tags = models.CharField(
        max_length=100, verbose_name="Tags (eg., recovery, nurse, detroitprotest, CollegeStudent... ) (separate with commas)", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.picture:
            picture = Image.open(self.picture)
            extension = os.path.splitext(self.picture.name)[-1]
            if extension.lower() == '.png':
                picture = picture.convert('RGB')

            if extension.lower() != '.png':
                if picture._getexif() is not None:
                    for a, b in picture._getexif().items():
                        if ExifTags.TAGS[a] == 'Orientation':
                            if b == 3:
                                picture = picture.rotate(180, expand=True)
                            elif b == 6:
                                picture = picture.rotate(270, expand=True)
                            elif b == 8:
                                picture = picture.rotate(90, expand=True)

            picture_io = io.BytesIO()
            picture.thumbnail((600, 600))
            picture.save(picture_io, quality=75, format="JPEG")
            resave = File(picture_io, name=self.picture.name)
            self.picture = resave
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse('story-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('story-detail', kwargs={'pk': self.story_id})

    def __str__(self):
        return self.text


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        comment_replied = Comment.objects.get(id=self.comment_id)
        return reverse('story-detail', kwargs={'pk': comment_replied.story_id})

    def __str__(self):
        return self.text
