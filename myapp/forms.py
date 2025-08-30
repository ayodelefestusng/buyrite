# forms.py
from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']



