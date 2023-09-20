from django import forms
from . models import Listing, Category, Comment, Bid

class CreateListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')

    class Meta:
        model = Listing
        fields = ['title', 'category', 'price', 'description', 'image']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']