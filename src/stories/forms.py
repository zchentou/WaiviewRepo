from django import forms
from django.contrib.auth.decorators import login_required
from .models import Story


class StoryCreateModelForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['issue_to_write_about', 'category_to_write_about',
                  'title', 'content_text', 'tags', 'picture', 'picture_caption']

    def clean(self):
        cleaned = super().clean()
        issue = cleaned.get('issue')
        category = cleaned.get('category')
        if category not in issue.categories.all():
            if_error = ''
            for category in issue.categories.all():
                add_on = f' {category}'
                if_error += f'{add_on}, '
            raise forms.ValidationError(
                f'Subcategories available for the topic {issue} are: {if_error}')


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
