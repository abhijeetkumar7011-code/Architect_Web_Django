from django.contrib import admin
from .models import (
    StudioInfo, Service, Project, ProjectImage,
    TeamMember, Testimonial, GalleryImage, ContactMessage
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(StudioInfo)
class StudioInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    ordering = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    ordering = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'role_or_company', 'order')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
