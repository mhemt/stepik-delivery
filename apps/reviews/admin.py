from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'text',
        'created_at',
        'published_at',
        'status',
    )
    list_filter = ('author', 'created_at', 'published_at')
    date_hierarchy = 'created_at'
