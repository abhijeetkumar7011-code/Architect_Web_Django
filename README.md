# Build Tech — Premium Studio Site (Rewritten)

## Run locally
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # to manage content via /admin/
python manage.py seed_demo         # optional: loads sample projects/services/team
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## What changed vs old version
- Brand new Django app structure (StudioInfo, Project, Service, TeamMember,
  Testimonial, GalleryImage, ContactMessage models) — fully manageable from /admin/.
- Editorial premium design system (ivory + charcoal + terracotta accent,
  Fraunces serif display type + Inter body) instead of Bootstrap defaults.
- Full-bleed hero, scroll-reveal animations, category-filterable project grid,
  numbered service list, dark testimonial/CTA bands.
- Old project's images reused as demo content via `seed_demo` management command.

## Adding real content
Go to /admin/, log in with your superuser, and fill in:
1. Studio Info (one entry — name, tagline, stats, contact details)
2. Services
3. Projects (mark some as "Featured" to show on homepage)
4. Team Members
5. Testimonials
6. Gallery Images

Then swap demo images for real photography in each model's image field.
