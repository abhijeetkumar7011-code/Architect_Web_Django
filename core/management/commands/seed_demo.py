from django.core.management.base import BaseCommand
from core.models import StudioInfo, Service, Project, TeamMember, Testimonial, GalleryImage


class Command(BaseCommand):
    help = "Seed demo content for preview"

    def handle(self, *args, **options):
        StudioInfo.objects.all().delete()
        Service.objects.all().delete()
        Project.objects.all().delete()
        TeamMember.objects.all().delete()
        Testimonial.objects.all().delete()
        GalleryImage.objects.all().delete()

        StudioInfo.objects.create(
            name="BUILD TECH",
            tagline="Architecture · Interiors · Urban Design",
            about_short="A multi-disciplinary studio crafting residential, commercial and urban projects rooted in context and material honesty.",
            about_long="Build Tech is a multi-disciplinary architecture and design practice founded on the belief that good design responds to climate, context and the people who use it. Over the years we've grown from small residential commissions into a studio trusted with commercial, institutional and urban-scale work, while keeping the same attention to detail we started with.",
            founded_year=2012,
            projects_count=120,
            awards_count=18,
            cities_count=9,
            email="info@buildtech.in",
            phone="+91 98765 43210",
            address="123 Main St, Delhi, India - 123456",
        )

        services_data = [
            ("Architecture Design", "Concept-to-construction architectural design for homes, offices and public buildings.", "architecture_design_icon.jpg"),
            ("Interior Design", "Material-led interiors that balance comfort, light and longevity.", "design_image.png"),
            ("Urban Planning", "Masterplanning and urban design for growing neighbourhoods and campuses.", "Office_Building.jpg"),
            ("Project Management", "On-ground execution oversight from groundbreaking to handover.", "business_building_icon.png"),
            ("Sustainability Consulting", "Passive design, material sourcing and energy strategy.", "housing.jpg"),
            ("Landscape Design", "Outdoor and landscape design integrated with the built form.", "image_2025-09-09_210147973.png"),
        ]
        services = []
        for title, summary, img in services_data:
            s = Service.objects.create(title=title, summary=summary, description=summary + " " + "We work closely with clients through every stage, combining technical rigor with design clarity.")
            s.cover_image.name = f"services/covers/{img}"
            s.save()
            services.append(s)

        projects_data = [
            ("Everest View Residence", "residential", "Manali, HP", 2023, "abstract-architecture-background-1.webp", True),
            ("Lakeside Boat House", "landscape", "Udaipur, RJ", 2022, "nice-landscape-with-boat.png", True),
            ("Civic Pavilion", "institutional", "Delhi, IN", 2021, "1543.jpg", True),
            ("Urban Loft Complex", "commercial", "Gurugram, HR", 2024, "2151933406.jpg", True),
            ("Material Study Facade", "interior", "Pune, MH", 2023, "abstract_architecture_detail.webp", False),
            ("Highland Retreat", "residential", "Shimla, HP", 2022, "beautiful-scenery-summit-mount-everest-covered-with-snow-white-clouds.jpg", True),
        ]
        for title, cat, loc, year, img, featured in projects_data:
            p = Project.objects.create(
                title=title, category=cat, location=loc, client="Private Client", year=year,
                area_sqft="8,500 sq ft", summary=f"A {cat} project completed in {loc} focused on light, material and context.",
                description="This project explores the relationship between built form and its surroundings, using local materials and passive design strategies to create spaces that feel inevitable rather than imposed.",
                is_featured=featured,
            )
            p.cover_image.name = f"projects/covers/{img}"
            p.save()
            p.services.add(services[hash(title) % len(services)])

        team_data = [
            ("Abhijeet Verma", "Founder & Principal Architect", "SDE.png"),
            ("Riya Sharma", "Senior Interior Designer", "sde_img.png"),
            ("Karan Mehta", "Urban Planner", "architecture_icon.png"),
            ("Ananya Iyer", "Project Manager", "er_icon.png"),
        ]
        for name, role, img in team_data:
            t = TeamMember.objects.create(name=name, role=role, bio=f"{name} brings deep expertise in {role.lower()} to every Build Tech project.")
            t.photo.name = f"team/{img}"
            t.save()

        testimonials_data = [
            ("Rohan Kapoor", "Homeowner, Manali", "Build Tech understood our brief better than we did. The result feels timeless, not trendy."),
            ("Meera Nair", "Director, Lakeview Hospitality", "Professional, on schedule, and the design quality exceeded what we briefed for."),
        ]
        for name, role, quote in testimonials_data:
            Testimonial.objects.create(client_name=name, role_or_company=role, quote=quote)

        gallery_imgs = ["DSC02870.JPG", "DSC02901.JPG", "DSC03003.JPG", "goa_beach.jpg", "ladakh_trip.webp", "mountain_trip.png"]
        for i, img in enumerate(gallery_imgs):
            g = GalleryImage.objects.create(title=f"Studio moment {i+1}", order=i)
            g.image.name = f"gallery/{img}"
            g.save()

        self.stdout.write(self.style.SUCCESS("Demo content seeded."))
