from django import template
from artworks.models import Photo, Topic, Type, CommentLink, ReplyLink, CommentPhoto, ReplyPhoto
from django.shortcuts import reverse

register = template.Library()


@register.filter
def return_all_types_for_topic(self):
    return self.types.all().order_by('position')


@register.filter
def all_topics(self):
    return Topic.objects.all().order_by('position')


@register.filter
def all_types(self):
    return Type.objects.all().order_by('position')


@register.filter
def only_topic(self, topic):
    return topic in self.path


@register.filter
def has_multiple_topics(self):
    for topic in Topic.objects.all():
        if topic.name in self.path:
            return False
    return True


@register.simple_tag
def photo_check_everything():
    return reverse('photo-list')


@register.simple_tag
def photo_check_topic_type_url(topic_name, type_name):
    check = reverse('photo-topic-type',
                    kwargs={'topic': topic_name, 'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def photo_check_type_all_topics_url(type_name):

    check = reverse('photo-type', kwargs={'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def photo_check_topic_all_types_url(topic_name):
    check = reverse('photo-topic', kwargs={'topic': topic_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def photo_mediatype_check_everything(request):
    media_type = 'BUG_SOMEWHERE_IF_THIS_SHOWS_UP'
    if 'picture' in request.path:
        media_type = 'picture'
    elif 'video' in request.path:
        media_type = 'video'
    check = reverse('photo-list-media_type', kwargs={'media_type': media_type})
    check = check.replace('%20', ' ')
    print(check)
    return check


@register.simple_tag
def photo_mediatype_check_topic_type_url(request, topic_name, type_name):
    media_type = 'BUG_SOMEWHERE_IF_THIS_SHOWS_UP'
    if 'picture' in request.path:
        media_type = 'picture'
    elif 'video' in request.path:
        media_type = 'video'
    check = reverse('photo-topic-type-media_type',
                    kwargs={'media_type': media_type, 'topic': topic_name, 'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def photo_mediatype_check_type_all_topics_url(request, type_name):
    media_type = 'BUG_SOMEWHERE_IF_THIS_SHOWS_UP'
    if 'picture' in request.path:
        media_type = 'picture'
    elif 'video' in request.path:
        media_type = 'video'
    check = reverse('photo-type-media_type',
                    kwargs={'media_type': media_type, 'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def photo_mediatype_check_topic_all_types_url(request, topic_name):
    media_type = 'BUG_SOMEWHERE_IF_THIS_SHOWS_UP'
    if 'picture' in request.path:
        media_type = 'picture'
    elif 'video' in request.path:
        media_type = 'video'
    check = reverse('photo-topic-media_type',
                    kwargs={'media_type': media_type, 'topic': topic_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def link_check_everything():
    return reverse('link-list')


@register.simple_tag
def link_check_topic_type_url(topic_name, type_name):
    check = reverse('link-topic-type',
                    kwargs={'topic': topic_name, 'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def link_check_type_all_topics_url(type_name):

    check = reverse('link-type', kwargs={'type': type_name})
    check = check.replace('%20', ' ')
    return check


@register.simple_tag
def link_check_topic_all_types_url(topic_name):
    check = reverse('link-topic', kwargs={'topic': topic_name})
    check = check.replace('%20', ' ')
    return check


@register.filter
def date_created_equal_to_last_updated(self):
    dateCreated = str(self.date_created)
    dateCreatedWithoutSeconds = dateCreated[:16]
    lastUpdated = str(self.last_updated)
    lastUpdatedWithoutSeconds = lastUpdated[:16]
    return dateCreatedWithoutSeconds == lastUpdatedWithoutSeconds


@register.filter
def search_is_alphabetical(self):
    return self.GET.get('list_order') == 'alphabetical'


@register.filter
def media_type_equal_to_picture(self):
    return 'picture' in self.path


@register.simple_tag
def media_type_in_url(request):

    if 'picture' in request.path:
        return 'picture'
    if 'video' in request.path:
        return 'video'


@register.filter
def num_comments_from_link(self):
    list = CommentLink.objects.filter(link_id=self.pk)
    return list.count()


@register.filter
def num_comments_from_photo(self):
    list = CommentPhoto.objects.filter(photo_id=self.pk)
    return list.count()


@register.filter
def num_comments_from_link_without_anonymous(self):
    list = CommentLink.objects.filter(link_id=self.pk, anonymous=false)
    return list.count()


@register.filter
def filter_repliesinthiscomment_exists(self, arg):
    return self.filter(comment_id=int(arg)).exists()


@register.filter
def get_link_id_from_reply(self):
    comment_replied = CommentLink.objects.get(id=self.comment_id)
    return comment_replied.link_id


@register.filter
def get_photo_id_from_reply(self):
    comment_replied = CommentPhoto.objects.get(id=self.comment_id)
    return comment_replied.photo_id


@register.filter
def am_date(self):
    return 'date' in self.path


@register.filter
def am_alphabetical(self):
    return 'alphabetical' in self.path
