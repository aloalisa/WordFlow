from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add your comment here...'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'section', 'image']