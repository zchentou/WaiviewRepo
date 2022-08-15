from django import template
from stories.models import Story, Comment
from artworks.models import Link, Photo, CommentLink, ReplyLink, CommentPhoto, ReplyLink
from profiles.models import Profile
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_story_title_from_comment(self):
    story = Story.objects.get(id=self.story_id)
    return story.title

@register.filter
def get_story_title_from_reply(self):
    comment_replied = Comment.objects.get(id=self.comment_id)
    story = Story.objects.get(id=comment_replied.story_id)
    return story.title

@register.filter
def get_link_title_from_comment(self):
    link = Link.objects.get(id=self.link_id)
    return link.title

@register.filter
def get_link_title_from_reply(self):
    comment_replied = CommentLink.objects.get(id=self.comment_id)
    link = Link.objects.get(id=comment_replied.link_id)
    return link.title

@register.filter
def get_photo_title_from_comment(self):
    photo = Photo.objects.get(id=self.photo_id)
    return photo.title

@register.filter
def get_photo_title_from_reply(self):
    comment_replied = CommentPhoto.objects.get(id=self.comment_id)
    photo = Photo.objects.get(id=comment_replied.photo_id)
    return photo.title

@register.filter
def get_profile_pic_url_from_story(self):
    profile = Profile.objects.get(user=User.objects.get(username=self.name))
    return profile.picture.url

@register.filter
def get_profile_pic_url_from_comment(self):
    profile = Profile.objects.get(user=User.objects.get(username=self.author))
    return profile.picture.url

@register.filter
def get_profile_pic_url_from_reply(self):
    profile = Profile.objects.get(user=User.objects.get(username=self.author))
    return profile.picture.url

@register.filter
def get_profile_pic_url_from_photo(self):
    profile = Profile.objects.get(user=User.objects.get(username=self.author))
    return profile.picture.url

@register.filter
def get_profile_pic_url_from_link(self):
    profile = Profile.objects.get(user=User.objects.get(username=self.author))
    return profile.picture.url
