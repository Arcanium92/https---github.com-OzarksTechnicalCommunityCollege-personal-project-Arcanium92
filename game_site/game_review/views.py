from django.shortcuts import render, get_object_or_404, redirect
from .models import GameReview
from .forms import ReviewForm

def home(request):
    return render(request, 'game_review/home.html')

def review_list(request):
    reviews = GameReview.objects.all()
    return render(request, 'game_review/review_list.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            return redirect('game_review:review_detail', pk=review.pk)
    else:
        form = ReviewForm()

    return render(request, 'game_review/add_review.html', {'form': form})

def review_detail(request, pk):
    review = get_object_or_404(GameReview, pk=pk)
    return render(request, 'game_review/review_detail.html', {'review': review})
