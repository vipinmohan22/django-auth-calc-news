from django import forms

from .models import Searchtopic, Newstopic, Comment


class SearchForm():
    query = forms.CharField(max_length=20, label='Query')

    class Meta:
        model = Searchtopic
        fields = ('query')


class NewsForm(forms.ModelForm):
    class Meta:
        model = Newstopic
        fields = ('Title', 'description',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)
