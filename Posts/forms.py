from django import forms

from Posts.models import Post, BlockedProfile


# Your forms go here


class PostsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        exclude = ('post_profile',)


class BlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BlockedProfile
        exclude = ('blocked_by', )

