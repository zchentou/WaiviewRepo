from django import forms
from .models import Photo, Topic, Type, Link


class PhotoCreateModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['topic', 'type', 'picture', 'video',
                  'title', 'picture_caption', 'tags']

    def clean(self):
        cleaned = super().clean()
        topic = cleaned.get('topic')
        type = cleaned.get('type')
        picture = cleaned.get('picture')
        video = cleaned.get('video')
        if type not in topic.types.all():
            if_error = ''
            for type in topic.types.all():
                add_on = f' {type}'
                if_error += f'{add_on}, '
            raise forms.ValidationError(
                f'Subcategories available for the topic {topic} are: {if_error}')

        if not bool(picture) and not bool(video):
            raise forms.ValidationError(
                'Please post either an image or video, you cannot share a media post without an image or video.')
        if bool(picture) and bool(video):
            raise forms.ValidationError(
                'Please post either an image or video. If you would like to post both an image and video, please do so separately as this will allow your posts to stay organized.')


class LinkCreateModelForm(forms.ModelForm):
    link_to_resource = forms.URLField(
        label='Link/URL to Resource', widget=forms.TextInput(attrs={'placeholder': 'Example: https://eji.org'}))
    title = forms.CharField(label='Title of Link/Resource', widget=forms.TextInput(
        attrs={'placeholder': 'Example: Equal Justice Initiative'}))

    class Meta:
        model = Link
        fields = ['topic', 'type', 'states_choices',
                  'link_to_resource', 'title', 'description', 'tags']

    def clean(self):
        cleaned = super().clean()
        topic = cleaned.get('topic')
        type = cleaned.get('type')
        if type not in topic.types.all():
            if_error = ''
            for type in topic.types.all():
                add_on = f' {type}'
                if_error += f'{add_on}, '
            raise forms.ValidationError(
                f'Subcategories available for this topic are: {if_error}')

    def clean_link_to_resource(self):
        link = self.cleaned_data.get('link_to_resource')
        if not link.startswith('http://') and not link.startswith('https://') and not link.startswith('ftp') and not link.startswith('ftps'):
            return f'http://{link}'
        else:
            return link


class RawCommentCreateForm(forms.Form):
    text = forms.CharField(label='', required=True, widget=forms.Textarea(
        attrs={
            "placeholder": "Add comment...",
            "rows": 5,
            "cols": 5
        }
    )
    )


class RawReplyCreateForm(forms.Form):
    text = forms.CharField(label='', required=True, widget=forms.Textarea(
        attrs={
            "placeholder": "Reply...",
            "rows": 5,
            "cols": 30
        }
    )
    )
