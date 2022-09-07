from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField


class BasicPage(Page):
    created = models.DateTimeField("Post date", auto_now_add=True)
    updated = models.DateTimeField("Updated date", auto_now=True)
    body = RichTextField(blank=True, null=True)
