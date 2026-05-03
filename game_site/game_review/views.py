import random, requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import GameReview
from .forms import ReviewForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def dashboard(request):
    return render(request, 'website/dashboard.html')

def review_list(request):
    reviews = GameReview.objects.all()
    return render(request, 'website/review_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    last_rating = request.COOKIES.get('last_rating')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()

            # Create redirect response so we can attach a cookie
            response = redirect('review_result', pk=review.pk)

            # Save rating submission in a cookie for 5 days
            response.set_cookie(
                'last_rating',
                review.rating,
                max_age=60*60*24*5
            )

            return response
    else:
        # Prefill rating if cookie exists
        form = ReviewForm(initial={'rating': last_rating})

    return render(request, 'website/add_review.html', {'form': form})

def review_result(request, pk):
    review = get_object_or_404(GameReview, pk=pk)
    return render(request, 'website/review_result.html', {'review': review})

# View for PokeAPI
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