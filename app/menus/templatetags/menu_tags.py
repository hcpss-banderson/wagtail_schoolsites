from django import template
from ..models import Menu
from wagtail.core.models import Site
from pprint import pprint

register = template.Library()


@register.simple_tag(takes_context=True)
def get_main_menu(context):
    return Menu.objects.get(title="Main", site_id=Site.find_for_request(context["request"]).id)


@register.simple_tag(takes_context=True)
def get_menu(context, slug):
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return None
