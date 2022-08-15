from django import template
from stories.models import Comment, Issue, Category
from django.shortcuts import reverse

register = template.Library()


@register.filter
def filter_covid_exists(self):
    return self.filter(issue_to_write_about='COVID').exists()


@register.filter
def filter_blm_exists(self):
    return self.filter(issue_to_write_about='BLM').exists()


@register.filter
def filter_repliesinthiscomment_exists(self, arg):
    return self.filter(comment_id=int(arg)).exists()


@register.filter
def get_story_id_from_reply(self):
    comment_replied = Comment.objects.get(id=self.comment_id)
    return comment_replied.story_id


@register.filter
def all_COVID_stories(self):
    return self.path == reverse('story-covid')


@register.filter
def all_BLM_stories(self):
    return self.path == reverse('story-BLM')


@register.filter
def only_COVID(self):
    return 'COVID' in self.path


@register.filter
def only_BLM(self):
    return 'blacklivesmatter' in self.path


@register.filter
def num_comments_from_story(self):
    list = Comment.objects.filter(story_id=self.pk)
    return list.count()


@register.filter
def num_comments_from_story_without_anonymous(self):
    list = Comment.objects.filter(story_id=self.pk, anonymous=false)
    return list.count()


@register.filter
def only_issue(self, issue):
    return issue in self.path


@register.filter
def has_multiple_issues(self):
    for issue in Issue.objects.all():
        if issue.name in self.path:
            return False
    return True


@register.filter
def all_issues(self):
    return Issue.objects.all().order_by('position')


@register.filter
def all_categories(self):
    return Category.objects.all().order_by('position')


@register.simple_tag
def check_issue_category_url(issue_name, category_name, content_type):
    check = reverse('story-issue-category', kwargs={'issue_to_write_about': issue_name,
                    'category_to_write_about': category_name, 'content_type': content_type})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def check_category_all_issues_url(category_name, content_type):
    check = reverse(
        'story-category', kwargs={'category_to_write_about': category_name, 'content_type': content_type})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def check_issue_all_categories_url(issue_name, content_type):
    return reverse('story-issue', kwargs={'issue_to_write_about': issue_name, 'content_type': content_type})


@register.simple_tag
def check_everything(content_type):
    return reverse('story-list', kwargs={'content_type': content_type})


@register.filter
def a_search(self):
    return self.GET.get('search_bar', '')


@register.filter
def return_all_categories_for_issue(self):

    return self.categories.all().order_by('position')


@register.filter
def date_created_equal_to_last_updated(self):
    dateCreated = str(self.date_created)
    dateCreatedWithoutSeconds = dateCreated[:16]
    lastUpdated = str(self.last_updated)
    lastUpdatedWithoutSeconds = lastUpdated[:16]
    return dateCreatedWithoutSeconds == lastUpdatedWithoutSeconds


@register.filter
def return_COVID_issue(self):
    return 'COVID-19'


@register.filter
def return_Frontline_Workers(self):
    return 'Frontline Workers'


@register.simple_tag
def content_type_in_url(request):

    if 'pictures' in request.path:
        return 'pictures'
    if 'everything' in request.path:
        return 'everything'
