from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image, ExifTags
import io
import os
from django.core.files import File


class Type(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=50)
    types = models.ManyToManyField(Type)
    position = models.IntegerField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, default=1, null=True)
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, default=1, verbose_name='Category', null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(
        upload_to='individual_imgs', verbose_name='Picture...', blank='True')
    video = models.FileField(upload_to='individual_vids',
                             verbose_name='...or Video', blank='True')
    title = models.CharField(max_length=70, blank=True,
                             verbose_name='Optional Title for Image/Video')
    picture_caption = models.CharField(
        max_length=1000, blank=True, verbose_name='Optional Caption for Image/Video')
    tags = models.CharField(
        max_length=100, verbose_name="Tags (eg., recovery, nurse, detroitprotest, CollegeStudent... ) (separate with commas)", blank=True)

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        if self.title:
            return self.title
        else:
            return f'No title, media from {self.author.username}'

    def save(self, *args, **kwargs):
        print(self.picture)
        if self.picture:
            picture = Image.open(self.picture)
            extension = os.path.splitext(self.picture.name)[-1]
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
            if extension.lower() == '.png':
                picture = picture.convert('RGB')
            picture_io = io.BytesIO()
            picture.thumbnail((600, 600))
            picture.save(picture_io, format="JPEG", quality=75)
            resave = File(picture_io, name=self.picture.name)
            self.picture = resave
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class Link(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, default=1, null=True)
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, default=1, verbose_name='Category', null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    link_to_resource = models.URLField(
        max_length=1500, verbose_name='Link/URL to Resource')

    states = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Minor Outlying Islands', 'Mississippi', 'Missouri', 'Montana',
              'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'U.S. Virgin Islands', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    states_initials = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO',
                       'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
    CHOICES_STATES = [(state, state) for state in states]

    states_choices = models.TextField(choices=CHOICES_STATES, blank=True,
                                      verbose_name='(If Applicable/Optional) The state/territory to which resource is specific to')

    title = models.CharField(
        max_length=70, verbose_name='Title of Link/Resource')
    description = models.TextField(
        verbose_name='Optional Description of Link/Resource', blank=True)
    tags = models.CharField(
        max_length=100, verbose_name="Tags (eg., mentalhealth, donate, protestinfo... ) (separate with commas)", blank=True)

    def get_absolute_url(self):
        return reverse('link-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class CommentLink(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('link-detail', kwargs={'pk': self.link_id})

    def __str__(self):
        return self.text


class ReplyLink(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentLink, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        comment_replied = CommentLink.objects.get(id=self.comment_id)
        return reverse('link-detail', kwargs={'pk': comment_replied.link_id})

    def __str__(self):
        return self.text


class CommentPhoto(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.photo_id})

    def __str__(self):
        return self.text


class ReplyPhoto(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentPhoto, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        comment_replied = CommentPhoto.objects.get(id=self.comment_id)
        return reverse('photo-detail', kwargs={'pk': comment_replied.photo_id})

    def __str__(self):
        return self.text
