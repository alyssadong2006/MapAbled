from django.contrib import admin
from .models import Location, Accessibility, Comment


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'geo_info',
        'name',
    )


@admin.register(Accessibility)
class AccessibilityAdmin(admin.ModelAdmin):
    list_display = ('feature', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'accessibility_rating',
        'likes',
        'dislikes',
    )
