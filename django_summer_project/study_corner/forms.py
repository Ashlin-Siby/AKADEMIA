from django import forms
from datetime import datetime


class MultiUsersForms(forms.Form):
    start = forms.IntegerField(label="Starting Roll No.", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    end = forms.IntegerField(label="Ending Roll No.", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))
    semester = forms.IntegerField(label="Semester", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(label="Batch Year", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        department = self.cleaned_data.get('department')
        semester = self.cleaned_data.get('semester')
        year = self.cleaned_data.get('year')

        currentYear = datetime.now().year

        if start > 99:
            raise forms.ValidationError("Input Starting Roll Number!!")
        elif end > 99:
            raise forms.ValidationError("Input End Roll Number!!")
        elif not department:
            raise forms.ValidationError("Enter Student Department!!")
        elif semester > 8:
            raise forms.ValidationError("Enter Student Semester!!")
        elif year>currentYear:
            raise forms.ValidationError("Enter Correct Year!!")
        return super(MultiUsersForms, self).clean()
