from django import forms

class NewPageForm(forms.Form):
    titlePage = forms.CharField(label = "Enter the page name")
    contentPage = forms.CharField(label = 'content', widget=forms.Textarea)

class EditPageForm(forms.Form):
    contentPage = forms.CharField(label = 'edit', widget=forms.Textarea)        