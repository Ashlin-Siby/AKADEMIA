from django import forms
from django.contrib.auth import get_user_model

from .models import MyCustomUser
from . import models

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta():
        model = MyCustomUser
        fields = ('username', 'email')

    def clean_password(self):
        password_1 = self.cleaned_data['password1']
        password_2 = self.cleaned_data['password2']
        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError("Password Mismatch.Please Enter password again")
        return password_2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user


class FileUploaderForm(forms.ModelForm):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user')
        user = self.user
        # new_choices = []
        if user.is_student and kwargs.pop('type_pk') != 'study_material':
            new_choices = (('notes', 'Notes'), ('question_paper', 'Question Papers'))

        elif user.is_staff:
            new_choices = (('study_material', 'Study Material'), ('question_paper', 'Question Papers'))

        super().__init__(**kwargs)
        self.fields['fileType'].choices = new_choices

    class Meta():
        model = models.Files
        fields = ('filePath', 'fileType', 'fileURL')
        widgets = {
            'filePath': forms.FileInput(attrs={'class': 'form-control-file'}),
            'fileType': forms.Select(attrs={'class': 'form-control'}),
            'fileURL': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ChangePasswordForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    oldPassword = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmPassword = forms.CharField(label='Confirm Password',
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self,**kwargs):
        query = self.cleaned_data.get('username')
        password = self.cleaned_data.get('oldPassword')
        newPassword = self.cleaned_data.get('newPassword')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        user_qs_final = User.objects.filter(username=query).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user doesn't exist!!!")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("Credentials aren't correct.")
        if newPassword != confirmPassword:
            raise forms.ValidationError("Password Mismatch!!!")
        self.cleaned_data['user_obj'] = user_obj
        return super(ChangePasswordForm, self).clean()
