from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserEmailCreationForm(UserCreationForm):
    """ User creating form to create a new user (adds email parameter) """
    # add email field to form 
    recovery_email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "recovery_email", "password1", "password2")

    # Save email on user creation 
    def save(self, commit=True):
        user = super(UserEmailCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["recovery_email"]
        if commit:
            user.save()
        return user