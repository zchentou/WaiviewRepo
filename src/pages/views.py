from django.shortcuts import render, reverse
from .models import Quote
from django.contrib import messages
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    ListView
)
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


def home_view(request):
    context = {}
    return render(request, 'home.html', context)


def about_view(request):
    context = {}
    return render(request, 'about.html', context)


def contact_view(request):
    context = {}
    return render(request, 'contact.html', context)


def acknowledgments_view(request):
    context = {}
    return render(request, 'acknowledgments.html', context)


def privacy_policy_view(request):
    context = {}
    return render(request, 'privacy_policy.html', context)


def terms_of_use_view(request):
    context = {}
    return render(request, 'terms_of_use.html', context)


def sitemap_view(request):
    context = {}
    return render(request, 'sitemap.xml', context)


class UserListView(ListView):
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        if self.request.method == "GET":
            input = self.request.GET.get('search_bar_user', '')
            if self.request.GET['people_search'] == 'users':
                if input == '':
                    return User.objects.all().order_by('username')
                else:
                    return User.objects.filter(username__icontains=input).order_by('username')
