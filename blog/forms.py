from django import forms
from .models import Blog_Post

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog_Post
        fields = ['title', 'description', 'solution', 'programming_language_tags']
        widgets={
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter title',
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Enter description of error',
                'rows':5
            }),
            'solution':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Enter solution'
            }),
            'programming_language_tags':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter programming language'
            }),

        }

def __init__(self, *args, **kwargs):
     super(BlogPostForm,self).__init__(*args,**kwargs)
     for field_name,field in self.fields.items():
         field.label_tag(attrs={'class':'text-success'})