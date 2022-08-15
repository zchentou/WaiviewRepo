from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import Http404
from .models import Photo, Link, Topic, Type, CommentPhoto, ReplyPhoto, CommentLink, ReplyLink
from .forms import PhotoCreateModelForm, LinkCreateModelForm, RawCommentCreateForm, RawReplyCreateForm
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Lower
from django.contrib.postgres.search import SearchVector, SearchQuery


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo

    def get_success_url(self):
        return reverse('photo-list')

    def test_func(self):
        photo = self.get_object()
        return photo.author == self.request.user


class PhotoListView(ListView):
    model = Photo
    ordering = ['-date_created']

    def get_paginate_by(self, queryset):

        if self.request.method == "GET":
            if self.request.GET.get('search_bar', ''):
                return 100
        return 12

    def get_queryset(self, *args, **kwargs):
        if self.request.method == "GET":
            input = self.request.GET.get('search_bar', '')
            if input:
                if self.request.GET['type_of_search'] == 'everything':
                    return Photo.objects.annotate(search=SearchVector('picture_caption', 'title', 'author__username', 'tags')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'title':
                    return Photo.objects.annotate(search=SearchVector('title')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'picture_caption':
                    return Photo.objects.annotate(search=SearchVector('picture_caption')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'author':
                    return Photo.objects.annotate(search=SearchVector('author__username')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'tags':
                    return Photo.objects.annotate(search=SearchVector('tags')).filter(search=SearchQuery(input)).order_by('-date_created')

        if self.kwargs.get('media_type') == 'picture':
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(topic=topic.id, type=type.id).exclude(picture='').order_by('-date_created')
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Photo.objects.filter(topic=topic.id).exclude(picture='').order_by('-date_created')
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(type=type.id).exclude(picture='').order_by('-date_created')
            else:
                return Photo.objects.exclude(picture='').order_by('-date_created')
        elif self.kwargs.get('media_type') == 'video':
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(topic=topic.id, type=type.id).exclude(video='').order_by('-date_created')
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Photo.objects.filter(topic=topic.id).exclude(video='').order_by('-date_created')
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(type=type.id).exclude(video='').order_by('-date_created')
            else:
                return Photo.objects.exclude(video='').order_by('-date_created')
        else:
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(topic=topic.id, type=type.id).order_by('-date_created')
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Photo.objects.filter(topic=topic.id).order_by('-date_created')
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Photo.objects.filter(type=type.id).order_by('-date_created')
            else:
                return Photo.objects.order_by('-date_created')


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoCreateModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        photo = self.get_object()
        return photo.author == self.request.user


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    form_class = LinkCreateModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Link

    def get_success_url(self):
        return reverse('link-list', kwargs={'order_type': 'date'})

    def test_func(self):
        link = self.get_object()
        return link.author == self.request.user


class LinkListView(ListView):
    model = Link

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_type'] = self.kwargs.get('order_type')
        return context

    def get_paginate_by(self, queryset):

        if self.request.method == "GET":
            if self.request.GET.get('search_bar', ''):
                return 100
        return 50

    def get_queryset(self, *args, **kwargs):
        if self.request.method == "GET":

            input = self.request.GET.get('search_bar', '')
            if input:
                if self.request.GET['type_of_search'] == 'everything':
                    return Link.objects.annotate(search=SearchVector('description', 'title', 'author__username', 'tags')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'title':
                    return Link.objects.annotate(search=SearchVector('title')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'description':
                    return Link.objects.annotate(search=SearchVector('description')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'author':
                    return Link.objects.annotate(search=SearchVector('author__username')).filter(search=SearchQuery(input)).order_by('-date_created')
                elif self.request.GET['type_of_search'] == 'tags':
                    return Link.objects.annotate(search=SearchVector('tags')).filter(search=SearchQuery(input)).order_by('-date_created')

        if self.kwargs.get('order_type') == 'alphabetical':
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(topic=topic.id, type=type.id).order_by(Lower('title'))
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Link.objects.filter(topic=topic.id).order_by(Lower('title'))
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(type=type.id).order_by(Lower('title'))
            else:
                return Link.objects.all().order_by(Lower('title'))
        elif self.kwargs.get('order_type') == 'date':
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(topic=topic.id, type=type.id).order_by('-date_created')
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Link.objects.filter(topic=topic.id).order_by('-date_created')
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(type=type.id).order_by('-date_created')
            else:
                return Link.objects.all().order_by('-date_created')

        else:
            if self.kwargs.get('topic') and self.kwargs.get('type'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(topic=topic.id, type=type.id).order_by('states_choices', '-date_created')
            elif self.kwargs.get('topic'):
                topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
                return Link.objects.filter(topic=topic.id).order_by('states_choices', '-date_created')
            elif self.kwargs.get('type'):
                type = get_object_or_404(Type, name=self.kwargs.get('type'))
                return Link.objects.filter(type=type.id).order_by('states_choices', '-date_created')
            else:
                return Link.objects.all().order_by('states_choices', '-date_created')


class LinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Link
    form_class = LinkCreateModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        link = self.get_object()
        return link.author == self.request.user


def LinkCommentsRepliesViewRaw(request, pk):

    object = get_object_or_404(Link, id=pk)
    comment_form = RawCommentCreateForm()
    reply_form = RawReplyCreateForm()
    comment_list = CommentLink.objects.filter(link_id=pk)

    reply_list = ReplyLink.objects.all()
    if request.method == "POST" and request.POST['theid'] == '0':
        if request.user.is_authenticated:
            comment_form = RawCommentCreateForm(request.POST)
            if comment_form.is_valid():
                CommentLink.objects.create(
                    **comment_form.cleaned_data, link_id=object.id, author_id=request.user.id)

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

                ReplyLink.objects.create(
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
    return render(request, "links/link_detail.html", context)


def PhotoCommentsRepliesViewRaw(request, pk):

    object = get_object_or_404(Photo, id=pk)

    comment_form = RawCommentCreateForm()
    reply_form = RawReplyCreateForm()
    comment_list = CommentPhoto.objects.filter(photo_id=pk)
    reply_list = ReplyPhoto.objects.all()
    if request.method == "POST" and request.POST['theid'] == '0':
        if request.user.is_authenticated:
            comment_form = RawCommentCreateForm(request.POST)
            if comment_form.is_valid():

                CommentPhoto.objects.create(
                    **comment_form.cleaned_data, photo_id=object.id, author_id=request.user.id)

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

                ReplyPhoto.objects.create(
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
    return render(request, "photos/photo_detail.html", context)


class CommentLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommentLink

    def get_success_url(self):
        return reverse('link-list')

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentLinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommentLink
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class ReplyLinkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReplyLink

    def get_success_url(self):
        return reverse('link-list')

    def test_func(self):
        reply = self.get_object()
        return reply.author == self.request.user


class ReplyLinkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReplyLink
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        reply = self.get_object()
        return reply.author == self.request.user


class CommentPhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommentPhoto

    def get_success_url(self):
        return reverse('photo-list')

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentPhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommentPhoto
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class ReplyPhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReplyPhoto

    def get_success_url(self):
        return reverse('photo-list')

    def test_func(self):
        reply = self.get_object()
        return reply.author == self.request.user


class ReplyPhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReplyPhoto
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        reply = self.get_object()
        return reply.author == self.request.user
