from django import forms

from .models import Searchtopic, Newstopic, Comment


class SearchForm(forms.ModelForm):
    class Meta:
        model = Searchtopic
        fields = ('search_query',)


class NewsForm(forms.ModelForm):
    class Meta:
        model = Newstopic
        fields = ('title', 'description',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)
