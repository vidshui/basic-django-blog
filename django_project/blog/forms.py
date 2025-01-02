# blog/forms.py

from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only the content field for now, as the user is automatically assigned

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your comment...'}),
        label='Your Comment'
    )
