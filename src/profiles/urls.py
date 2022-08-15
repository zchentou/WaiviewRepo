from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile'),
    path('<str:username>/stories/', views.ProfileStoryListView.as_view(template_name='profiles/profile_story_list.html'), name='profile-story-list'),
    path('<str:username>/comments/', views.ProfileStoryCommentListView.as_view(template_name='profiles/profile_comment_list.html'), name='profile-comment-list'),
    path('<str:username>/replies/', views.ProfileStoryReplyListView.as_view(template_name='profiles/profile_reply_list.html'), name='profile-reply-list'),

    path('<str:username>/images/', views.ProfilePhotoListView.as_view(template_name='profiles/profile_photo_list.html'), name='profile-photo-list'),
    path('<str:username>/images/comments/', views.ProfilePhotoCommentListView.as_view(template_name='profiles/profile_comment_list_photo.html'), name='profile-comment-list-photo'),
    path('<str:username>/images/replies/', views.ProfilePhotoReplyListView.as_view(template_name='profiles/profile_reply_list_photo.html'), name='profile-reply-list-photo'),

    path('<str:username>/links/', views.ProfileLinkListView.as_view(template_name='profiles/profile_link_list.html'), name='profile-link-list'),
    path('<str:username>/links/comments/', views.ProfileLinkCommentListView.as_view(template_name='profiles/profile_comment_list_link.html'), name='profile-comment-list-link'),
    path('<str:username>/links/replies/', views.ProfileLinkReplyListView.as_view(template_name='profiles/profile_reply_list_link.html'), name='profile-reply-list-link'),

    path('<str:username>/delete/', views.user_delete_view, name='profile-delete'),
    path('<str:username>/email/delete/', views.email_delete_view, name='account_email_delete'),
]
