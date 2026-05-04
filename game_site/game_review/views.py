import random, requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import GameReview, ReviewLike
from .forms import ReviewForm

# Dashboard (with recently viewed)
def dashboard(request):
    viewed_ids = request.session.get('viewed_reviews', [])
    recently_viewed = GameReview.objects.filter(id__in=viewed_ids)

    return render(request, 'website/dashboard.html', {
        "recently_viewed": recently_viewed
    })

# Review List (with pagination)
def review_list(request):
    reviews = GameReview.objects.all()

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'website/review_list.html', {
        "page_obj": page_obj
    })

# Add Review (cookie memory)
@login_required
def add_review(request):
    last_rating = request.COOKIES.get('last_rating')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()

            response = redirect('review_result', pk=review.pk)

            response.set_cookie(
                'last_rating',
                review.rating,
                max_age=60*60*24*5
            )

            return response
    else:
        form = ReviewForm(initial={'rating': last_rating})

    return render(request, 'website/add_review.html', {'form': form})

# Review Result (post-submit)
def review_result(request, pk):
    review = get_object_or_404(GameReview, pk=pk)
    return render(request, 'website/review_result.html', {'review': review})

# Review Detail (likes + caching + recently viewed)
def review_detail(request, review_id):
    review = get_object_or_404(GameReview, id=review_id)

    # Track recently viewed
    viewed = request.session.get('viewed_reviews', [])
    if review_id not in viewed:
        viewed.append(review_id)
    request.session['viewed_reviews'] = viewed

    # Cache like count
    like_count = review.like_count

    return render(request, 'website/review_detail.html', {
        "review": review,
        "like_count": like_count
    })

# Toggle Like
@login_required
def toggle_like(request, review_id):
    review = get_object_or_404(GameReview, id=review_id)
    user = request.user

    existing_like = ReviewLike.objects.filter(user=user, review=review).first()

    if existing_like:
        existing_like.delete()
    else:
        ReviewLike.objects.create(user=user, review=review)

    return redirect('review_detail', review_id=review_id)

# Pokémon API
def random_pokemon(request):
    pokemon_id = random.randint(1, 151)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    response = requests.get(url).json()

    data = {
        "name": response["name"].title(),
        "sprite": response["sprites"]["front_default"],
        "hp": response["stats"][0]["base_stat"],
        "attack": response["stats"][1]["base_stat"],
        "defense": response["stats"][2]["base_stat"],
    }

    return JsonResponse(data)