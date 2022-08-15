from django.urls import path
from . import views

urlpatterns = [
    path('images/create/', views.PhotoCreateView.as_view(
        template_name='photos/photo_create.html'), name='photo-create'),
    path('images/<int:pk>/delete/', views.PhotoDeleteView.as_view(
        template_name='photos/photo_confirm_delete.html'), name='photo-delete'),
    path('images/<int:pk>/', views.PhotoCommentsRepliesViewRaw, name='photo-detail'),
    path('images/', views.PhotoListView.as_view(template_name='photos/photo_list.html'), name='photo-list'),
    path('images/topic/type/<str:topic>/<str:type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list.html'), name='photo-topic-type'),
    path('images/topic/<str:topic>/', views.PhotoListView.as_view(
        template_name='photos/photo_list.html'), name='photo-topic'),
    path('images/type/<str:type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list.html'), name='photo-type'),
    path('images/<str:media_type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list_media_type.html'), name='photo-list-media_type'),
    path('images/topic/type/<str:topic>/<str:type>/<str:media_type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list_media_type.html'), name='photo-topic-type-media_type'),
    path('images/topic/<str:topic>/<str:media_type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list_media_type.html'), name='photo-topic-media_type'),
    path('images/type/<str:type>/<str:media_type>/', views.PhotoListView.as_view(
        template_name='photos/photo_list_media_type.html'), name='photo-type-media_type'),
    path('images/<int:pk>/update/', views.PhotoUpdateView.as_view(
        template_name='photos/photo_create.html'), name='photo-update'),
    path('images/<int:pk>/comments/delete/', views.CommentPhotoDeleteView.as_view(
        template_name='photos/comment_confirm_delete.html'), name='photo-comment-delete'),
    path('images/<int:pk>/comments/update/', views.CommentPhotoUpdateView.as_view(
        template_name='photos/comment_update.html'), name='photo-comment-update'),
    path('images/<int:pk>/replies/delete/', views.ReplyPhotoDeleteView.as_view(
        template_name='photos/reply_confirm_delete.html'), name='photo-reply-delete'),
    path('images/<int:pk>/replies/update/', views.ReplyPhotoUpdateView.as_view(
        template_name='photos/comment_update.html'), name='photo-reply-update'),
    path('links/create/', views.LinkCreateView.as_view(
        template_name='links/link_create.html'), name='link-create'),
    path('links/<int:pk>/delete/', views.LinkDeleteView.as_view(
        template_name='links/link_confirm_delete.html'), name='link-delete'),
    path('links/<int:pk>/', views.LinkCommentsRepliesViewRaw, name='link-detail'),
    path('links/all/<str:order_type>/', views.LinkListView.as_view(
        template_name='links/link_list.html'), name='link-list'),
    path('links/topic/type/<str:topic>/<str:type>/<str:order_type>/',
         views.LinkListView.as_view(template_name='links/link_list.html'), name='link-topic-type'),
    path('links/topic/<str:topic>/<str:order_type>/',
         views.LinkListView.as_view(template_name='links/link_list.html'), name='link-topic'),
    path('links/type/<str:type>/<str:order_type>/',
         views.LinkListView.as_view(template_name='links/link_list.html'), name='link-type'),
    path('links/<int:pk>/update/', views.LinkUpdateView.as_view(
        template_name='links/link_create.html'), name='link-update'),
    path('links/<int:pk>/comments/delete/', views.CommentLinkDeleteView.as_view(
        template_name='links/comment_confirm_delete.html'), name='link-comment-delete'),
    path('links/<int:pk>/comments/update/', views.CommentLinkUpdateView.as_view(
        template_name='links/comment_update.html'), name='link-comment-update'),
    path('links/<int:pk>/replies/delete/', views.ReplyLinkDeleteView.as_view(
        template_name='links/reply_confirm_delete.html'), name='link-reply-delete'),
    path('links/<int:pk>/replies/update/', views.ReplyLinkUpdateView.as_view(
        template_name='links/reply_update.html'), name='link-reply-update'),

]
