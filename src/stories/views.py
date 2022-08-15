from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Story, Comment, Reply, Issue, Category
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator
from .forms import RawCommentCreateForm, RawReplyCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.utils.timezone import activate
from django.conf import settings
from django.utils import timezone


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    fields = ['issue_to_write_about', 'category_to_write_about',
              'title', 'content_text', 'tags', 'picture', 'picture_caption']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Story

    def get_success_url(self):
        return reverse('story-list', kwargs={'content_type': 'everything'})

    def test_func(self):
        story = self.get_object()
        return story.name == self.request.user


class StoryDetailView(DetailView):
    model = Story
    queryset = Story.objects.all()


class StoryListView(ListView):
    model = Story
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = self.kwargs.get('content_type')
        return context

    def get_paginate_by(self, queryset):
        if self.request.method == "GET":
            if self.request.GET.get('search_bar', ''):
                return 100
        if 'pictures' in self.request.path:
            return 12
        return 6

    def get_queryset(self, *args, **kwargs):
        if self.request.method == "GET":
            input = self.request.GET.get('search_bar', '')
            if input:
                if self.request.GET['type_of_search'] == 'everything':
                    return Story.objects.annotate(search=SearchVector('content_text', 'title', 'name__username', 'tags')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'title':
                    return Story.objects.annotate(search=SearchVector('title')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'content_text':
                    return Story.objects.annotate(search=SearchVector('content_text')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'name':
                    return Story.objects.annotate(search=SearchVector('name__username')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'tags':
                    return Story.objects.annotate(search=SearchVector('tags')).filter(search=SearchQuery(input)).order_by('-date_created')

        if self.kwargs.get('content_type') == 'everything':
            if self.kwargs.get('issue_to_write_about') and self.kwargs.get('category_to_write_about'):
                issue = get_object_or_404(
                    Issue, name=self.kwargs.get('issue_to_write_about'))
                category = get_object_or_404(
                    Category, name=self.kwargs.get('category_to_write_about'))
                return Story.objects.filter(issue_to_write_about=issue.id, category_to_write_about=category.id).order_by('-date_created')
            elif self.kwargs.get('issue_to_write_about'):
                issue = get_object_or_404(
                    Issue, name=self.kwargs.get('issue_to_write_about'))
                return Story.objects.filter(issue_to_write_about=issue.id).order_by('-date_created')
            elif self.kwargs.get('category_to_write_about'):
                category = get_object_or_404(
                    Category, name=self.kwargs.get('category_to_write_about'))
                return Story.objects.filter(category_to_write_about=category.id).order_by('-date_created')
            else:
                return Story.objects.all().order_by('-date_created')
        else:
            if self.kwargs.get('issue_to_write_about') and self.kwargs.get('category_to_write_about'):
                issue = get_object_or_404(
                    Issue, name=self.kwargs.get('issue_to_write_about'))
                category = get_object_or_404(
                    Category, name=self.kwargs.get('category_to_write_about'))
                return Story.objects.filter(issue_to_write_about=issue.id, category_to_write_about=category.id).exclude(picture='').order_by('-date_created')
            elif self.kwargs.get('issue_to_write_about'):
                issue = get_object_or_404(
                    Issue, name=self.kwargs.get('issue_to_write_about'))
                return Story.objects.filter(issue_to_write_about=issue.id).exclude(picture='').order_by('-date_created')
            elif self.kwargs.get('category_to_write_about'):
                category = get_object_or_404(
                    Category, name=self.kwargs.get('category_to_write_about'))
                return Story.objects.filter(category_to_write_about=category.id).exclude(picture='').order_by('-date_created')
            else:
                return Story.objects.exclude(picture='').order_by('-date_created')


class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Story
    fields = ['issue_to_write_about', 'category_to_write_about',
              'title', 'content_text', 'tags', 'picture', 'picture_caption']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        story = self.get_object()
        return story.name == self.request.user


def StoryCommentsViewRaw(request, pk):
    object = get_object_or_404(Story, id=pk)
    form = RawCommentCreateForm()
    comment_list = Comment.objects.filter(story_id=pk)
    if request.method == "POST":
        form = RawCommentCreateForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                **form.cleaned_data, story_id=object.id, author_id=request.user.id)
            return redirect(object.get_absolute_url())
        else:
            print(form.errors)
    context = {
        'object': object,
        "form": form,
        'comment_list': comment_list
    }
    return render(request, "stories/story_detail.html", context)


def CommentRepliesViewRaw(request, pk, id):
    object = get_object_or_404(Comment, id=id)
    form = RawReplyCreateForm()
    reply_list = Reply.objects.filter(comment_id=id)
    if request.method == "POST":
        form = RawReplyCreateForm(request.POST)
        if form.is_valid():
            Reply.objects.create(
                **form.cleaned_data, comment_id=object.id, author_id=request.user.id)
            return redirect(object.get_absolute_url())
        else:
            print(form.errors)
    context = {
        'object': object,
        "form": form,
        'reply_list': reply_list
    }
    return render(request, "stories/comments/comment_detail.html", context)


def StoryCommentsRepliesViewRaw(request, pk):
    object = get_object_or_404(Story, id=pk)
    comment_form = RawCommentCreateForm()
    reply_form = RawReplyCreateForm()
    comment_list = Comment.objects.filter(story_id=pk)
    reply_list = Reply.objects.all()
    if request.method == "POST" and request.POST['theid'] == '0':
        if request.user.is_authenticated:
            comment_form = RawCommentCreateForm(request.POST)
            if comment_form.is_valid():
                Comment.objects.create(
                    **comment_form.cleaned_data, story_id=object.id, author_id=request.user.id)
                return redirect(object.get_absolute_url())
            else:
                print(form.errors)
        else:
            messages.warning(
                request, f'You need to be logged in to post comments.')
            return redirect(reverse('account_login'))
    if request.method == "POST" and request.POST['theid'] != '0':
        if request.user.is_authenticated:
            reply_form = RawReplyCreateForm(request.POST)
            if reply_form.is_valid():
                Reply.objects.create(
                    **reply_form.cleaned_data, comment_id=int(request.POST['theid']), author_id=request.user.id)
                return redirect(object.get_absolute_url())
            else:
                print(form.errors)
        else:
            messages.warning(
                request, f'You need to be logged in to post replies.')
            return redirect(reverse('account_login'))

    context = {
        'object': object,
        "comment_form": comment_form,
        'reply_form': reply_form,
        'comment_list': comment_list,
        'reply_list': reply_list
    }
    return render(request, "stories/story_detail.html", context)


def user_story_list_view(request, username):
    queryset = Story.objects.filter(name=username)
    context = {
        "object_list": queryset,
        "username": username
    }
    return render(request, 'stories/user_story_list.html', context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('story-list', kwargs={'content_type': 'everything'})

    def test_func(self):

        comment = self.get_object()
        return comment.author == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):

        comment = self.get_object()
        return comment.author == self.request.user


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reply

    def get_success_url(self):
        return reverse('story-list', kwargs={'content_type': 'everything'})

    def test_func(self):

        reply = self.get_object()
        return reply.author == self.request.user


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):

        reply = self.get_object()
        return reply.author == self.request.user
