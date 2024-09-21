from django.utils import timezone
from django import forms
from .models import AuctionListing


class CreateListingForm(forms.ModelForm):
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Select the end date and time for the auction."
    )
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_price', 'image', 'category', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'starting_price': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['category'].required = False

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date <= timezone.now():
            raise forms.ValidationError("End date must be in the future.")
        return end_date