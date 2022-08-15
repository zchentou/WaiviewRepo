from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileForm, UserDeleteForm, EmailDeleteForm
from django.contrib import messages
from stories.models import Story, Comment, Reply
from artworks.models import Photo, Link, CommentPhoto, ReplyPhoto, CommentLink, ReplyLink
from django.contrib.auth.models import User
from .models import Profile
from django.core.paginator import Paginator

from django.views.generic import (
    ListView,
)

import pytz
from allauth.account.models import EmailAddress


class ProfileLinkReplyListView(ListView):
    model = ReplyLink
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ReplyLink.objects.filter(author=user).order_by('-date_created')


class ProfileLinkCommentListView(ListView):
    model = CommentLink
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return CommentLink.objects.filter(author=user).order_by('-date_created')


class ProfileLinkListView(ListView):
    model = Link
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Link.objects.filter(author=user).order_by('-date_created')


class ProfilePhotoReplyListView(ListView):
    model = ReplyPhoto
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ReplyPhoto.objects.filter(author=user).order_by('-date_created')


class ProfilePhotoCommentListView(ListView):
    model = CommentPhoto
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return CommentPhoto.objects.filter(author=user).order_by('-date_created')


class ProfilePhotoListView(ListView):
    model = Photo
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Photo.objects.filter(author=user).order_by('-date_created')


class ProfileStoryReplyListView(ListView):
    model = Reply
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reply.objects.filter(author=user).order_by('-date_created')


class ProfileStoryCommentListView(ListView):
    model = Comment
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Comment.objects.filter(author=user).order_by('-date_created')


class ProfileStoryListView(ListView):
    model = Story
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_of_profile'] = User.objects.get(
            username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Story.objects.filter(name=user).order_by('-date_created')


def profile_view(request, username):
    context = {}
    if request.method == "POST":

        if request.user.is_authenticated:
            if request.user == User.objects.get(username=username):
                my_u_form = UserUpdateForm(request.POST, instance=request.user)
                my_p_form = ProfileForm(
                    request.POST, request.FILES, instance=request.user.profile)
                if my_u_form.is_valid() and my_p_form.is_valid():
                    my_u_form.save()

                    my_p_form.save()
                    messages.success(
                        request, f'Your profile has successfully been changed!')

                    return redirect('profile', username=request.user.username)

                else:

                    context = {
                        'user_form': my_u_form,
                        'profile_form': my_p_form,
                        "user_of_profile": User.objects.get(username=username)
                    }
                    return render(request, 'profiles/profile.html', context)
    else:

        if request.user.is_authenticated:
            my_u_form = UserUpdateForm(instance=request.user)
            my_p_form = ProfileForm(instance=request.user.profile)
            context = {
                'user_form': my_u_form,
                'profile_form': my_p_form,
                "user_of_profile": User.objects.get(username=username)
            }
            return render(request, 'profiles/profile.html', context)
        else:

            my_u_form = UserUpdateForm(
                instance=User.objects.get(username=username))
            my_p_form = ProfileForm(
                instance=User.objects.get(username=username).profile)
            context = {
                'user_form': my_u_form,
                'profile_form': my_p_form,
                "user_of_profile": User.objects.get(username=username)
            }
            return render(request, 'profiles/profile.html', context)


def user_delete_view(request, username):
    if request.user.is_authenticated:
        if request.user == User.objects.get(username=username):
            form = UserDeleteForm()
            context = {
                'form': form,
                "user_of_profile": User.objects.get(username=username)
            }

            if request.method == "POST":
                form = UserDeleteForm(request.POST)
                if form.is_valid():
                    if form.cleaned_data['delete_sure'] == True:
                        user_to_delete = User.objects.get(username=username)
                        user_to_delete.delete()
                        messages.success(
                            request, f'Your account with username {username} has been deleted. Thank you for having used our website!')
                        return redirect('story-list', content_type='everything')
                    else:
                        messages.warning(
                            request, f'If you want to delete your account, please select the checkbox and press that you are sure.')
                        return redirect('profile-delete', username=username)
                else:
                    print(form.errors)
            else:
                return render(request, 'profiles/user_delete.html', context)
        else:
            messages.warning(
                request, 'This url is unavailable to you. Make sure to select your profile if you want to delete your account.')
            return redirect('story-list', content_type='everything')
    else:
        messages.warning(
            request, 'This url is unavailable to you. Make sure to select your profile if you want to delete your account.')
        return redirect('story-list', content_type='everything')


def email_delete_view(request, username):
    if request.user.is_authenticated:
        if request.user == User.objects.get(username=username):
            form = EmailDeleteForm()
            context = {
                'form': form,
                "user_of_profile": User.objects.get(username=username)
            }

            if request.method == "POST":
                form = EmailDeleteForm(request.POST)
                if form.is_valid():
                    if form.cleaned_data['delete_sure'] == True:
                        user_whose_email_to_delete = User.objects.get(
                            username=username)
                        user_whose_email_to_delete.email = ''
                        user_whose_email_to_delete.save()
                        for email_of_user_allauth in EmailAddress.objects.filter(user=request.user):
                            email_of_user_allauth.delete()
                        messages.success(
                            request, f'Your emails for your account with username {username} has been removed')
                        return redirect('profile', username=username)
                    else:
                        messages.warning(
                            request, f'If you want to remove your emails, please select the checkbox and press that you are sure.')
                        return redirect('account_email_delete', username=username)
                else:

                    print(form.errors)
            else:
                return render(request, 'profiles/email_delete.html', context)
        else:
            messages.warning(
                request, 'This url is unavailable to you. Make sure to select your profile if you want to remove your emails.')
            return redirect('story-list', content_type='everything')
    else:
        messages.warning(
            request, 'This url is unavailable to you. Make sure to select your profile if you want to remove your emails.')
        return redirect('story-list', content_type='everything')
