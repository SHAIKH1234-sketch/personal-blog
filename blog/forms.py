from django import forms
from .models import Comments
class CommentsForm(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=['post']
        label={
        "user_name":"Your Naame",
        "user_email":"Your Email",
        "text":"Your Comments",
        }
