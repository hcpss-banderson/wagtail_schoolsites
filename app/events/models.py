from django.db import models
from wagtail.models import Page
from news.models import News
from home.models import Feature
from wagtail.fields import RichTextField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class EventListingPage(Page):
    """List events."""

    template = "events/events_listing_page.html"
    max_count = 1
    subpage_types = ["events.Event"]

    @property
    def get_child_pages(self):
        return Event.objects.descendant_of(self).live().order_by("-start_date")

    def get_sitemap_urls(self, request=None):
        return []


class Event(Feature):
    """Event model."""

    subpage_types = []
    parent_page_types = ['events.EventListingPage']

    start_date = models.DateTimeField("Start time")
    end_date = models.DateTimeField("End time")

    search_fields = Page.search_fields + [
        index.FilterField('start_date'),
        index.FilterField('end_date'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
    ]

    def full_clean(self, *args, **kwargs):
        """Generate slug."""

        super(Event, self).full_clean(*args, **kwargs)

        prefix = '{:%Y-%m-%d-}'.format(self.start_date)

        if not self.slug.startswith(prefix):
            self.slug = prefix + self.slug
