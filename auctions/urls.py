from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive_listings", views.inactive_listings, name="inactive_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:pk>/view/", views.listing_detail_view, name="listing_detail_view"),
    path("auctions/categories/", views.categories, name="categories"),
    path("auctions/categories/<str:category>/", views.listing_by_category,name="listing_by_category"),
    path("auctions/add_to_watch_list/<int:id>/", views.add_to_watch_list,name="add_to_watch_list"),
    path("auctions/remove_from_watch_list/<int:id>/", views.remove_from_watch_list,name="remove_from_watch_list"),
    path("auctions/remove_from_category/<int:id>/", views.remove_from_category,name="remove_from_category"),
    path("auctions/watch_list/", views.watch_list, name="watch_list"),
    path("auctions/listing/<int:pk>/update/", views.ListingUpdateView.as_view(), name="update_listing"),
    path("auctions/listing/<int:id>/close/", views.close_listing, name="close_listing"),
    path("auctions/comments/<int:pk>/update/", views.CommentUpdateView.as_view(), name="update_comment"),
    path("auctions/listing/<int:id>/like/", views.like_listing, name="like_listing"),
    path("auctions/listings/search", views.search, name="search"),
    path("auctions/listings/search_result", views.search_result, name="search_result")
]
