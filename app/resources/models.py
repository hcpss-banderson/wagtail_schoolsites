from django.db import models
from wagtail.core.models import Orderable, CollectionMember
from wagtail.admin.edit_handlers import MultiFieldPanel, InlinePanel, FieldPanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.models.sites import Site


class Resource(Orderable):
    title = models.CharField(blank=True, null=True, max_length=100)
    url = models.URLField(max_length=500, blank=True)
    description = models.CharField(max_length=500, blank=True)
    list = ParentalKey("ResourceList", related_name="resources")

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("description"),
    ]


@register_snippet
class ResourceList(ClusterableModel, CollectionMember):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("icon"),
            FieldPanel("site"),
        ], heading="Resource List"),
        InlinePanel("resources", label="Resources"),
    ]

    def __str__(self):
        return self.title
