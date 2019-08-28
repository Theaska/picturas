from django.contrib.auth.models import User
from django import forms
from blog.models import Post, Comment
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

class PostForm(forms.ModelForm):
    max_size_img = 5

    class Meta:
        model = Post
        fields = ['description', 'image']
        labels = {
            'description': _('Описание поста'),
            'image': _('Выберите файл'),
        } 
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание поста'}),
            'image': forms.ClearableFileInput(attrs={'type': "file", 'class': "form-control-file"})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise ValidationError("Файл должен быть не больше {0} мб".format(self.max_size_img))
            return image
        else:
            raise ValidationError("Не удалось прочитать файл")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст комментария'})
            }



