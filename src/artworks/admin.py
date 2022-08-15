from django.contrib import admin
from .models import Topic, Type, Photo, Link, CommentLink, ReplyLink, CommentPhoto, ReplyPhoto
# Register your models here.

admin.site.register(Topic)
admin.site.register(Type)
admin.site.register(Photo)
admin.site.register(Link)
admin.site.register(CommentLink)
admin.site.register(ReplyLink)
admin.site.register(CommentPhoto)
admin.site.register(ReplyPhoto)
