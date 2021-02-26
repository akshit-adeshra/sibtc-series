from django import forms
from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.models import User
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2', 'is_staff', 'tnc')
        # Whichever fields you want to display in your SignUp Form, you have to add that field's name in this list here,
        # .. and that field name already needs to be a built-in field or already defined in accounts/models.py file.

        # As the field is already a built-in field or you just defined it in accounts/models.py, it's data is going to
        # .. be saved in the database, but to see it in the django admin panel, you have to add that field's name in the
        # .. "fieldsets" field in the admin.py file

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #
    #     try:
    #         match = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return email
    #
    #     raise forms.ValidationError('This email is not in the database..!!')
