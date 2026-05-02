from django import forms
from .models import GameReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = GameReview
        fields = ['title', 'review_text', 'rating']