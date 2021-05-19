from django import forms
from .models import Category

categories = Category.objects.values_list('id', 'name')


class NewListingForm(forms.Form):
    listing_title = forms.CharField(label='Listing Title', max_length=100)
    listing_discription = forms.CharField(label='Description', widget=forms.Textarea)
    start_bid = forms.FloatField(label="Start Bid")
    listing_image = forms.CharField( max_length=600)
    category = forms.MultipleChoiceField(
        label="Categories",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=categories,
    )

        
class BindListing(forms.Form):
    price_bind = forms.FloatField(label="Price")

class CommentListing(forms.Form):
    comment = forms.CharField(label='Comment', widget=forms.Textarea)

class WatchListing(forms.Form):
    wl = forms.CharField(
        widget=forms.HiddenInput(),
        required = False,
        initial="teste"
    )

class IsUser(forms.Form):
    close = forms.CharField(
        widget=forms.HiddenInput(),
        required = False,
        initial="close"
    )

   