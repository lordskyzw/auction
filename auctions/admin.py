from django.contrib import admin
from . models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ['listed_by', 'title', 'price', 'category', 'date_created']
    search_fields = ['listed_by', 'title', 'price', 'category', 'description', 'image']
admin.site.register(Listing, ListingAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
admin.site.register(User, UserAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['listing', 'commentator', 'message', 'date_commented']
    search_fields = ['commentator__user_name', 'listing__title']
admin.site.register(Comment, CommentAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ['listing', 'bidder', 'price', 'date_bid']
    search_fields = ['listing__title', 'bidder__user_name']
admin.site.register(Bid, BidAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'added_by']
admin.site.register(Category, CategoryAdmin)