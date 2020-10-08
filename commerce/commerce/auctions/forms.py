from django import forms

class Add_Listing(forms.Form):
    add = forms.HiddenInput(label='Your name')