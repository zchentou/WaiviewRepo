from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image, ImageFilter, ExifTags
import pytz
import io
import os
from django.core.files import File


def unique_file_path(instance, filename):
    return os.path.join(f'/profile_imgs/{instance.user.username}/', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=50, blank=True)

    picture = models.ImageField(default='profile_imgs/default_img.png',
                                upload_to='profile_imgs', verbose_name='Profile Picture', blank=True)
    OPTIONS = [(time, time) for time in pytz.common_timezones]
    timezone_to_use = models.CharField(
        max_length=30, choices=OPTIONS, default='US/Eastern')

    ONECOL = 'ONE'
    TWOCOL = 'TWO'
    VIEW_CHOICE = [
        (ONECOL, 'View one story in each row (stories stacked on each other)'),
        (TWOCOL, 'View two stories in same row (two stories inline next to each other)')
    ]
    choice_view = models.CharField(
        max_length=3,
        choices=VIEW_CHOICE,
        default=TWOCOL,
        verbose_name='Choose how you want to see stories of others laid out (only applies to larger screens such as laptops and tablets)'
    )

    terms = models.BooleanField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        pic_in_update = False
        if 'update_fields' in kwargs:
            if "picture" in kwargs['update_fields']:
                pic_in_update = True

        if self.picture and (not 'update_fields' in kwargs or pic_in_update) and self.picture.name != 'profile_imgs/default_img.png':

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
            picture.thumbnail((350, 350))
            picture.save(picture_io, format="JPEG", quality=80)
            resave = File(picture_io, name=self.picture.name)
            self.picture = resave
            super().save(*args, **kwargs)
        else:
            self.picture.name = 'profile_imgs/default_img.png'
            super().save(*args, **kwargs)
