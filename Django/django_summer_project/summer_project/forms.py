from django import forms
from .models import MyCustomUser


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
