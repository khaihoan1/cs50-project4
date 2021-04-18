from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = request.user
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs=({
                'rows': '2',
                'class': 'post-create-input',
                'placeholder': "What's on your mind?"
            }))
        }
        labels = {
            'content': ''
        }

    def save(self):
        return super().save(commit=False)
        # new_post.owner = user
        # print("ahihi", new_post.content, new_post.count_like, new_post.owner)
        # return new_post
# class PostForm(forms.Form):
#     content = forms.TextInput()
