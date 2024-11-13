from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import (User, Listing, Comment, Bid, Category, WatchList)
from .forms import (
    CreateListingForm, CommentForm, BiddingForm, CreateCategoryForm
)


def index(request):
    listings = Listing.objects.filter(active=True).order_by("-date_created")
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user
        ).count()
    else:
        watch_list_total = 0
    top_listings = Listing.objects.all().filter(
        active=True
    ).order_by('-price')[:10]
    listings = Paginator(listings, 10)
    page = request.GET.get('page')
    try:
        listings = listings.page(page)
    except:
        listings = listings.page(1)
    
    if request.method == 'POST':
        create_listing_form = CreateListingForm(request.POST, request.FILES)
        if create_listing_form.is_valid():
            if not request.user.is_authenticated:
                messages.error(request, "You must be signed in before you can create a listing")
                return HttpResponseRedirect(reverse('index'))
            admin_user = User.objects.get(username='example')# Replace 'admin_username' with the actual admin username
            if request.user != admin_user:
                messages.error(request, "Only the admin can create listings.")
                return HttpResponseRedirect(reverse('index'))
            create_listing_form.instance.listed_by = request.user
            create_listing_form.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/index.html", {
        'listings': listings, 'create_listing_form': CreateListingForm, 'top_listings': top_listings, 'watch_list_total':watch_list_total
    })

def inactive_listings(request):
    listings = Listing.objects.all().filter(
        active=False
    ).order_by('-date_created')
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user
        ).count()
    else:
        watch_list_total = 0
    top_listings = Listing.objects.all().filter(
        active=True
    ).order_by('-price')[:10]
    listings = Paginator(listings, 10)
    page = request.GET.get('page')
    try:
        listings = listings.page(page)
    except:
        listings = listings.page(1)
    
    if request.method == 'POST':
        ...

    return render(request, "auctions/inactive_listings.html", {
        'listings': listings, 'top_listings': top_listings,
        'watch_list_total':watch_list_total
    })


def login_view(request):
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user
        ).count()
    else:
        watch_list_total = 0
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, f"You are successfully logged in, {username}")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                'watch_list_total': watch_list_total
            })
    else:
        return render(request, "auctions/login.html", {
            'watch_list_total': watch_list_total
        })


def logout_view(request):
    username = request.user.username
    logout(request)
    messages.warning(request, f"You are successfully logged out, {username}")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user).count()
    else:
        watch_list_total = 0
    if request.user.is_authenticated:
        messages.error(request, f"You are already registered and signed in as {request.user.username}")
        return (HttpResponseRedirect(reverse("index")))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Make sure the user fill out the entire registration form
        if not username or not email:
            messages.error(request, "Please fill out the username and email")
            return HttpResponseRedirect(reverse("register"))

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                'watch_list_total': watch_list_total
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                'watch_list_total': watch_list_total
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            'watch_list_total': watch_list_total
        })

def listing_detail_view(request, pk):
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user).count()
    else:
        watch_list_total = 0
    listing = Listing.objects.filter(pk=pk).first()
    if request.user.is_authenticated:
        in_watch_list = WatchList.objects.filter(
            listing=listing, watched_by=request.user
        ).first()
    else:
        in_watch_list = True
    top_listings = Listing.objects.all().order_by('-price')[:10]
    comments = Comment.objects.filter(listing=listing).order_by('-listing__date_created').all()
    bids = Bid.objects.filter(listing=listing).order_by('-price').all()
    if not listing:
        messages.error(request, "No such listing is available")
        return HttpResponseRedirect(reverse("index"))
    liked = False
    if listing.likes.filter(id=request.user.id).exists():
        liked = True
    total_likes = listing.total_likes()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must sign in before you could do that")
            return HttpResponseRedirect(reverse('listing_detail_view', args=(listing.id, )))
        comment_form = CommentForm(request.POST)
        bidding_form = BiddingForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.commentator = request.user
            comment_form.instance.listing = listing
            comment_form.save()
            messages.success(request, "You have commented successfully")
            return HttpResponseRedirect(reverse('listing_detail_view', args=(pk, )))
        if bidding_form.is_valid():
            bidding_form.instance.bidder = request.user
            bidding_form.instance.listing = listing
            if bidding_form.instance.price <= listing.price:
                messages.error(
                    request, "Sorry you can't bid with that amount. \
                            Your amount must be greater than all other bids")
                return HttpResponseRedirect(reverse('listing_detail_view', args=(pk, )))
            if bidding_form.instance.price > listing.price:
                listing.price = bidding_form.instance.price
                listing.current_bidder = request.user
                listing.save()
                messages.success(request, "Hooray! Your bid is the current bid")
            else:
                messages.success(request, "You have successfully placed your bid")
            bidding_form.save()
            return HttpResponseRedirect(reverse('listing_detail_view', args=(pk, )))
    return render(request, "auctions/listing_detail_view.html", {
        "listing": listing, 'top_listings': top_listings, 'comments': comments,
        'comment_form': CommentForm, 'bidding_form': BiddingForm, 'bids': bids,
        'watch_list_total': watch_list_total, 'in_watch_list': in_watch_list,
        'liked': liked, 'total_likes': total_likes
    })

def categories(request):
    if request.user.is_authenticated:
        watch_list_total = WatchList.objects.filter(
            watched_by=request.user).count()
    else:
        watch_list_total = 0
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        create_category_form = CreateCategoryForm(request.POST)
        if create_category_form.is_valid():
            if not request.user.is_authenticated:
                messages.error(request, "You must be signed in before you can create a category")
                return HttpResponseRedirect(reverse('categories'))
            create_category_form.instance.added_by = request.user
            create_category_form.save()
            messages.success(request, "Category added successfully")
            return HttpResponseRedirect(reverse('categories'))
    return render(request, "auctions/categories.html", {
        'categories': categories, 'create_category_form': CreateCategoryForm,
        'watch_list_total': watch_list_total
    })

def listing_by_category(request, category):
    listings = Listing.objects.filter(category__name=category).all().order_by('-date_created')
    top_listings = Listing.objects.all().order_by('-price')[:10]

    listings = Paginator(listings, 10)
    page = request.GET.get('page')
    try:
        listings = listings.page(page)
    except:
        listings = listings.page(1)
    if not listings:
        messages.error(request, "Sorry no listings matched that category")
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/listings_by_category.html", {
        'listings': listings, 'category': category, 'top_listings': top_listings
    })

@login_required
def watch_list(request):
    watch_listed_items = WatchList.objects.all().filter(
        watched_by=request.user
    )
    watch_list_total = WatchList.objects.filter(
        watched_by=request.user).count()
    top_listings = Listing.objects.all().order_by('-price')[:10]
    return render(request, "auctions/watch_list.html", {
        "watch_listed_items": watch_listed_items, "top_listings": top_listings,
        'watch_list_total': watch_list_total
    })

@login_required
def add_to_watch_list(request, id):
    item = Listing.objects.get(id=id)
    watch_listing = WatchList(listing=item, watched_by=request.user)
    watch_listing.save()
    messages.success(request, "Item added to watched lists")
    return HttpResponseRedirect(reverse('listing_detail_view', args=(id,)))


@login_required
def remove_from_watch_list(request, id):
    listing = get_object_or_404(WatchList, id=id, watched_by=request.user)
    listing.delete()
    messages.success(request, "Item removed from watched lists")
    return HttpResponseRedirect(reverse('watch_list'))

@login_required
def remove_from_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Item removed from categories")
    return HttpResponseRedirect(reverse('categories'))

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    fields = ['title', 'category', 'price', 'description', 'image']

    def form_valid(self, form):
        form.instance.listed_by = self.request.user
        messages.success(self.request, "Listing updated successfully")
        return super().form_valid(form)
    
    def test_func(self):
        listing = self.get_object()
        return listing.listed_by == self.request.user
    
    def get_context_data(self, *args, **kwargs):
        context = super(ListingUpdateView, self).get_context_data(*args, **kwargs)
        watch_list_total = WatchList.objects.filter(
        watched_by=self.request.user).count()
        top_listings = Listing.objects.all().order_by('-price')[:10]
        context['watch_list_total'] = watch_list_total
        context['top_listings'] = top_listings
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.all().order_by('name')
        return form

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['message']

    def form_valid(self, form):
        form.instance.commentator = self.request.user
        messages.success(self.request, "Comment updated successfully")
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return comment.commentator == self.request.user
    
    def get_context_data(self, *args, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(*args, **kwargs)
        watch_list_total = WatchList.objects.filter(
        watched_by=self.request.user).count()
        top_listings = Listing.objects.all().order_by('-price')[:10]
        context['watch_list_total'] = watch_list_total
        context['top_listings'] = top_listings
        return context

@login_required
def close_listing(request, id):
    listing = get_object_or_404(Listing, id=id, listed_by=request.user)
    listing.active = False
    listing.save()
    messages.success(request, "Listing closed successfully")
    return HttpResponseRedirect(reverse('inactive_listings'))

@login_required
def like_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if listing.likes.filter(id=request.user.id).exists():
        listing.likes.remove(request.user)
    else:
        listing.likes.add(request.user)
    return HttpResponseRedirect(reverse('listing_detail_view', args=(listing.id,)))

def search(request):
    listings = Listing.objects.all()
    return render(request, "auctions/search.html", {
        "listings": listings
    })

def search_result(request):
    query = request.GET.get('search', '')
    listings = Listing.objects.all()
    if query:
        searched = listings.filter(
            title__icontains=query,
        )
    else:
        searched = []
    return render(request, "auctions/search_result.html", {
        "searched": searched
    })
    