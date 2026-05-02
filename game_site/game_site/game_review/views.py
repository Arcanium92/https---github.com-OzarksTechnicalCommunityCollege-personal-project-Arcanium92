from django.shortcuts import render, redirect, get_object_or_404
from .models import GameReview
from .forms import ReviewForm

def dashboard(request):
    return render(request, 'website/dashboard.html')

def review_list(request):
    reviews = GameReview.objects.all()
    return render(request, 'website/review_list.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            return redirect('game_review:review_result', pk=review.pk)
    else:
        form = ReviewForm()

    return render(request, 'website/add_review.html', {'form': form})

def review_result(request, pk):
    review = get_object_or_404(GameReview, pk=pk)
    return render(request, 'website/review_result.html', {'review': review})
