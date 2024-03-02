from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'desc', 'intro', 'body', 'image1', 'image2']  # Adjust fields as needed
