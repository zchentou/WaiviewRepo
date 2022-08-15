from django.shortcuts import reverse
from django import template
from stories.models import Story
from pages.models import Quote

register = template.Library()


@register.filter
def am_home(self):
    return self.path == reverse('home')


@register.filter
def am_about_us(self):
    return self.path == reverse('about')


@register.filter
def am_contact_us(self):
    return self.path == reverse('contact')


@register.filter
def am_profile(self):
    return self.path == reverse('profile', self.user.username)


@register.filter
def am_images(self):
    return self.path == reverse('photo-list')


@register.filter
def am_post(self):
    return self.path == reverse('story-create') or self.path == reverse('photo-create') or self.path == reverse('link-create')


@register.filter
def am_account_login(self):
    return self.path == reverse('account_login')


@register.filter
def am_account_signup(self):
    return self.path == reverse('account_signup')


@register.filter
def am_account_logout(self):
    return self.path == reverse('account_logout')


@register.filter
def daily_quote_text(self):
    quote = Quote.objects.get(current_daily='True')
    return quote.text


@register.filter
def daily_quote_storyid(self):
    quote = Quote.objects.get(current_daily='True')
    return quote.story_id


@register.filter
def story_object_from_daily_quote_anonymous(self):
    quote = Quote.objects.get(current_daily='True')
    story = Story.objects.get(id=quote.story_id)
    return story.anonymous


@register.filter
def story_object_from_daily_quote_title(self):
    quote = Quote.objects.get(current_daily='True')
    story = Story.objects.get(id=quote.story_id)
    return story.title


@register.filter
def story_object_from_daily_quote_name(self):
    quote = Quote.objects.get(current_daily='True')
    story = Story.objects.get(id=quote.story_id)
    return story.name


@register.filter
def divide(self, arg):
    return int(self / arg)
