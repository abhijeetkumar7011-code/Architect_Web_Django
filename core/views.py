from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import (
    StudioInfo, Service, Project, TeamMember,
    Testimonial, GalleryImage
)
from .forms import ContactForm


def get_studio_info():
    return StudioInfo.objects.first()


def home(request):
    context = {
        'studio': get_studio_info(),
        'featured_projects': Project.objects.filter(is_featured=True)[:6],
        'services': Service.objects.all()[:6],
        'testimonials': Testimonial.objects.all()[:5],
        'gallery_images': GalleryImage.objects.all()[:8],
        'contact_form': ContactForm(),
    }
    return render(request, 'core/home.html', context)


class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['studio'] = get_studio_info()
        ctx['categories'] = Project.CATEGORY_CHOICES
        ctx['active_category'] = self.request.GET.get('category', '')
        return ctx


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['studio'] = get_studio_info()
        ctx['next_project'] = Project.objects.exclude(pk=self.object.pk).order_by('?').first()
        return ctx


class ServiceListView(ListView):
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['studio'] = get_studio_info()
        return ctx


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['studio'] = get_studio_info()
        ctx['related_projects'] = self.object.projects.all()[:4]
        ctx['next_service'] = Service.objects.exclude(pk=self.object.pk).order_by('?').first()
        return ctx


def team(request):
    context = {
        'studio': get_studio_info(),
        'team_members': TeamMember.objects.all(),
    }
    return render(request, 'core/team.html', context)


def about(request):
    context = {
        'studio': get_studio_info(),
        'team_members': TeamMember.objects.all()[:4],
        'testimonials': Testimonial.objects.all(),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out — we'll be in touch shortly.")
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'studio': get_studio_info(),
        'form': form,
    }
    return render(request, 'core/contact.html', context)
