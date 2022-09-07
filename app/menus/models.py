from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import MultiFieldPanel, InlinePanel, FieldPanel, PageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.models import Orderable, CollectionMember
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.utils.text import slugify
from wagtail.models.sites import Site


class MenuItem(Orderable):
    link_title = models.CharField(blank=True, null=True, max_length=100)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    page = ParentalKey("Menu", related_name="menu_items")
    title_of_submenu = models.CharField(blank=True, null=True, max_length=50, help_text="Leave blank if there is no submenu")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("title_of_submenu"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self) -> str:
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"

    @property
    def slug_of_submenu(self):
        if self.title_of_submenu:
            return slugify(self.title_of_submenu)
        return None


@register_snippet
class Menu(ClusterableModel, CollectionMember):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    s = models.SlugField(unique=False)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
            FieldPanel("site")
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
