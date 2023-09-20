from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return (self.username)
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            image.thumbnail((300, 300))
            image.save(self.image.path)

# To categorize the listings
class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    price = models.FloatField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(default='auction_pics/default.png', upload_to='auction_pics')
    date_created = models.DateField(default=timezone.now)
    current_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="current_bidder")
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name="listings", blank=True)

    def __str__(self):
        return (self.title)
    
    def get_absolute_url(self):
        return reverse('listing_detail_view', args=(self.pk,))
    
    def save(self, *args, **kwargs):
        super(Listing, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            image.thumbnail((300, 300))
            image.save(self.image.path)
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    date_commented = models.DateField(default=timezone.now)

    def __str__(self):
        return (self.listing.title)
    
    def get_absolute_url(self):
        return reverse('listing_detail_view', args=(self.listing.id,))

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.FloatField()
    date_bid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.listing)

class WatchList(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watch_listings")
    watched_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.listing.title