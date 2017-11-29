from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


def validate_comment(value):
    wordlist = []
    f = open('djangotask/files/flaggit.txt', 'r')
    for line in f:
        for word in line.split():
            wordlist.append(word)
    f.close()
    if any(word in value for word in wordlist):
        raise ValidationError(
            _('%(value)s is not allowed'),
            params={'value': value},
        )


class Newstopic(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='newstopic')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.title


class Searchtopic(models.Model):
    search_query = models.CharField(max_length=20)


class Comment(models.Model):
    news = models.ForeignKey('newsapp.Newstopic', related_name='newscomment')
    author = models.ForeignKey(User, related_name='newstopiccomment', null=True)
    text = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def clean(self):
        validate_comment(self.text)
