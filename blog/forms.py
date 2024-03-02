from django import forms

from blog.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name': 'Your name',
            'user_email': 'Your email',
            'text': 'Comment'
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'date', 'slug']
        labels = {
            'title': 'Title',
            'excerpt': 'Short description',
            'image_name': 'Image',
            'content': 'Content',
            'tags': 'Tags'
        }

        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
