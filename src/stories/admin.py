from django.contrib import admin
from .models import Story, Comment, Reply, Issue, Category

admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Issue)
admin.site.register(Category)
