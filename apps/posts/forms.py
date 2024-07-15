from django import forms
from apps.posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content', 'media']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['post_content'].label = ""
        self.fields['media'].label = ""
