from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudioInfo(models.Model):
    """Singleton-style model for global studio info, shown across site/footer."""
    name = models.CharField(max_length=120, default="STUDIO NAME")
    tagline = models.CharField(max_length=200, blank=True)
    about_short = models.TextField(blank=True, help_text="2-3 line intro shown on home hero")
    about_long = models.TextField(blank=True, help_text="Full about text for About page")
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    projects_count = models.PositiveIntegerField(default=0, help_text="Stat shown on home, e.g. 120")
    awards_count = models.PositiveIntegerField(default=0)
    cities_count = models.PositiveIntegerField(default=0)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    map_embed_url = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    behance = models.URLField(blank=True)

    class Meta:
        verbose_name = "Studio Info"
        verbose_name_plural = "Studio Info"

    def __str__(self):
        return self.name


class Service(TimeStamped):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=240, help_text="Short one-liner for cards")
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='services/icons/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='services/covers/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class Project(TimeStamped):
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('interior', 'Interior'),
        ('landscape', 'Landscape'),
        ('urban', 'Urban Planning'),
        ('institutional', 'Institutional'),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='residential')
    location = models.CharField(max_length=120, blank=True)
    client = models.CharField(max_length=120, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    area_sqft = models.CharField(max_length=60, blank=True, help_text="e.g. 12,000 sq ft")
    summary = models.CharField(max_length=240, blank=True, help_text="One-line shown on listing/cards")
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='projects/covers/')
    services = models.ManyToManyField(Service, blank=True, related_name='projects')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-year']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - image {self.order}"


class TeamMember(TimeStamped):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Testimonial(TimeStamped):
    client_name = models.CharField(max_length=120)
    role_or_company = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.client_name


class GalleryImage(models.Model):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Gallery image {self.id}"


class ContactMessage(TimeStamped):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"
