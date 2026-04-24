from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape
from .models import (
    HeroSlide, Project, Advantage,
    PartnerProject, GalleryImage, PerspectiveInfo, SiteSettings,
)
from .forms import ContactForm


def index(request):
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'projects': Project.objects.all(),
        'advantages': Advantage.objects.all(),
        'partner_projects': PartnerProject.objects.all(),
        'gallery_images': GalleryImage.objects.all(),
        'gallery_realized': GalleryImage.objects.filter(category='realized'),
        'gallery_completed': GalleryImage.objects.filter(category='completed'),
        'gallery_perspective': GalleryImage.objects.filter(category='perspective'),
        'perspective': PerspectiveInfo.load(),
        'contact_form': ContactForm(),
    }
    return render(request, 'index.html', context)


def contact_submit(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        s = SiteSettings.load()
        # Без animate-fade-up: динамічний вміст через HTMX не потрапляє в IntersectionObserver
        # і залишається з opacity:0 без класу is-visible.
        return HttpResponse(
            '<div class="form-success" role="status" aria-live="polite">'
            '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
            '<path d="M20 6L9 17l-5-5"/>'
            '</svg>'
            f'<p>{escape(s.contact_success_title)}</p>'
            f'<p>{escape(s.contact_success_text)}</p>'
            '</div>'
        )

    _mark_error_fields(form)
    return render(request, 'partials/_contact_form.html', {'form': form}, status=422)


def _mark_error_fields(form):
    for field_name, field in form.fields.items():
        widget = form.fields[field_name].widget
        css = widget.attrs.get('class', '')
        if form[field_name].errors:
            if 'form-input--error' not in css:
                widget.attrs['class'] = f'{css} form-input--error'.strip()
        else:
            widget.attrs['class'] = css.replace('form-input--error', '').strip()
