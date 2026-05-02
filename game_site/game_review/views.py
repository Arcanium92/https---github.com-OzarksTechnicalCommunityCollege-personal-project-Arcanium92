from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from .models import GameReview, ReviewLike
from .forms import GameReviewForm, UserRegistrationForm
from .serializers import GameReviewSerializer
from django.core.paginator import Paginator
from django.core.cache import cache
from rest_framework import viewsets

# Adding these for API responses
import random, requests
from django.http import JsonResponse

# Adding decorators for user login
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def home(request):
    viewed_ids = request.session.get('viewed_reviews', [])
    recently_viewed = GameReview.objects.filter(id__in=viewed_ids)
    return render(request, "review/home.html", {
        "recently_viewed": recently_viewed
    })

"""This section is for user account settings"""
# Account registration function
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            # Creates new user object
            new_user = user_form.save(commit=False)

            # Set password
            new_user.set_password(user_form.cleaned_data['password'])

            # Save user
            new_user.save()

            user = authenticate(
                username=new_user.username,
                password=user_form.cleaned_data['password']
            )
            login(request, user)

            return redirect('home')

    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'user_form': user_form}
    )

# Function to pull GameReview objects and prefetches likes
def get_reviews_with_likes():
    like_qs = ReviewLike.objects.select_related('user')
    return GameReview.objects.all().prefetch_related(
        Prefetch('likes', queryset=like_qs)
    ).order_by('-submission')

# Pagination view
def paginate_queryset(request, queryset, per_page=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)

# Reworked current_user view for like/unlike
def attach_current_user(page_obj, user):
    for review in page_obj:
        review.current_user = user
    return page_obj

# Reworked review_list view
def review_list(request):
    reviews = get_reviews_with_likes()
    page_obj = paginate_queryset(request, reviews)
    page_obj = attach_current_user(page_obj, request.user)
    return render(request, "review/review_list.html", {"page_obj": page_obj})

# Make login required for add_review page and uses the form validation and saves the review
@login_required
def add_review(request):
    last_rating = request.COOKIES.get('last_rating')

    if request.method == "POST":
        form = GameReviewForm(request.POST)
        if form.is_valid():
            review = form.save()

            response = redirect("review_result", pk=review.pk)

            # Save rating submission in a cookie for 5 days
            response.set_cookie(
                'last_rating',
                review.rating,
                max_age=60*60*24*5
            )

            return response
    else:
        form = GameReviewForm(initial={'rating': last_rating})

    return render(request, "add_review/add_review.html", {"form": form})

# displays a list of all game reviews and pulls all of the objects from the database to the template
def review_result(request, pk):
    review = GameReview.objects.get(pk=pk)
    return render(request, "review/review_result.html", {"review": review})

# function to cache likes
def review_detail(request, review_id):
    review = get_object_or_404(GameReview, id=review_id)
    #Track recently viewed reviews
    viewed = request.session.get('viewed_reviews', [])

    if review_id not in viewed:
        viewed.append(review_id)

    request.session['viewed_reviews'] = viewed

    # Cache Logic
    key = f"review:{review_id}:like_count"
    like_count = cache.get(key)

    if like_count is None:
        like_count = review.like_count
        cache.set(key, like_count, 30)

    return render(request, "review/detail.html", {
        "review": review,
        "like_count": like_count
    })


# Toggle like/unlike view
@login_required
def toggle_like(request, review_id):
    review = get_object_or_404(GameReview, id= review_id)
    user = request.user
    existing_like = ReviewLike.objects.filter(user=user, review=review).first()
    
    if existing_like:
        existing_like.delete()
    else:
        ReviewLike.objects.create(user=user, review=review)
    return redirect('review_list')

# View for APIs
class GameReviewSets(viewsets.ModelViewSet):
    queryset = GameReview.objects.all()
    serializer_class = GameReviewSerializer

# View for PokeAPI data soon to be tied to button on home.html
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