from django import template

register = template.Library()


@register.filter
def webp(url):
    """
    Transforms a Cloudinary image URL to use f_auto,q_auto transformations.
    Non-Cloudinary URLs are returned as-is.
    """
    if not url:
        return url
    url = str(url)
    marker = '/image/upload/'
    if 'res.cloudinary.com' in url and marker in url:
        return url.replace(marker, f'{marker}f_auto,q_auto/', 1)
    return url
