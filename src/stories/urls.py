from django.urls import path
from .models import Story
from . import views

urlpatterns = [
    path('create/', views.StoryCreateView.as_view(template_name='stories/story_create.html'), name='story-create'),
    path('<int:pk>/delete/', views.StoryDeleteView.as_view(), name='story-delete'),
    path('<int:pk>/', views.StoryCommentsRepliesViewRaw, name='story-detail'),
    path('all/<str:content_type>/', views.StoryListView.as_view(), name='story-list'),
    path('issue/category/<str:issue_to_write_about>/<str:category_to_write_about>/<str:content_type>/', views.StoryListView.as_view(), name='story-issue-category'),
    path('issue/<str:issue_to_write_about>/<str:content_type>/', views.StoryListView.as_view(), name='story-issue'),
    path('category/<str:category_to_write_about>/<str:content_type>/', views.StoryListView.as_view(), name='story-category'),
    path('<int:pk>/update/', views.StoryUpdateView.as_view(template_name='stories/story_create.html'), name='story-update'),
    path('<int:pk>/comments/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/comments/update/', views.CommentUpdateView.as_view(template_name='stories/comment_update.html'), name='comment-update'),
    path('<int:pk>/replies/delete/', views.ReplyDeleteView.as_view(), name='reply-delete'),
    path('<int:pk>/replies/update/', views.ReplyUpdateView.as_view(template_name='stories/comment_update.html'), name='reply-update')
]
