from django.forms import ModelForm
from .models import User


class PersonalInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'bio', 'avatar_pic')
