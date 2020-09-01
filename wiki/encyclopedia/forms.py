from django import forms

class NewPageForm(forms.Form):
    titlePage = forms.CharField(label = "Enter the page name")
    contentPage = forms.CharField(label = 'll', widget=forms.Textarea)