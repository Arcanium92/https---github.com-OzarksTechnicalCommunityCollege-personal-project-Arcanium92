from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ReviewLike, GameReview

@receiver(post_save, sender=ReviewLike)
def increment_like_count(sender, instance, created, **kwargs):
    if created:
        review = instance.review
        review.like_count += 1
        review.save(update_fields=['like_count'])

@receiver(post_delete, sender=ReviewLike)
def decrement_like_count(sender, instance, **kwargs):
    review = instance.review
    if review.like_count > 0:
        review.like_count -= 1
        review.save(update_fields=['like_count'])