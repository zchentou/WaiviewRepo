from django.db import models
from stories.models import Story
from django.contrib.auth.models import User


class Quote(models.Model):
    text = models.TextField()
    story = models.ForeignKey(
        Story, blank=True, null=True, on_delete=models.CASCADE)
    current_daily = models.BooleanField()

    def __str__(self):
        if self.current_daily and self.story:
            return f'CURRENT- Quote from {self.story} is current being used!'
        elif self.current_daily:
            return 'CURRENT- Quote from outside is current being used!'
        elif self.story:
            return f'Quote from {self.story}'
        else:
            return f'Quote from outside'
