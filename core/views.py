from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
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
        thank_url = reverse('thank_you')
        if request.headers.get('HX-Request', '').strip().lower() == 'true':
            response = HttpResponse(status=200)
            response['HX-Redirect'] = thank_url
            return response
        return redirect('thank_you')

    _mark_error_fields(form)
    return render(request, 'partials/_contact_form.html', {'form': form}, status=422)


def thank_you(request):
    return render(request, 'thank_you.html')


def _mark_error_fields(form):
    for field_name, field in form.fields.items():
        widget = form.fields[field_name].widget
        css = widget.attrs.get('class', '')
        if form[field_name].errors:
            if 'form-input--error' not in css:
                widget.attrs['class'] = f'{css} form-input--error'.strip()
        else:
            widget.attrs['class'] = css.replace('form-input--error', '').strip()
