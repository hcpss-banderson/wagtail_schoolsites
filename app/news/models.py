from django.db import models
from wagtail.models import Page
from home.models import Feature
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime


class Tag(TaggedItemBase):
    id = models.AutoField(primary_key=True)
    content_object = ParentalKey('news.News', on_delete=models.CASCADE, related_name='tagged_items')


class NewsListingPage(RoutablePageMixin, Page):
    """List the news pages."""
    template = "news/news_listing_page.html"
    max_count = 1
    subpage_types = ["news.News"]

    @property
    def get_child_pages(self):
        return News.objects.descendant_of(self).live().order_by("-first_published_at")

    def get_context(self, request, *args, **kwargs):
        """Add stuff to our context."""

        context = super().get_context(request, *args, **kwargs)
        all_posts = self.posts if hasattr(self, 'posts') else News.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 10)
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        return context

    def get_sitemap_urls(self, request=None):
        return []


class News(Feature):
    """News detail page."""

    page_description = "Don't front act like you know"

    subpage_types = []
    parent_page_types = ['news.NewsListingPage']

    created = models.DateTimeField("Post date", auto_now_add=True)
    updated = models.DateTimeField("Updated date", auto_now=True)
    tags = ClusterTaggableManager(through=Tag, blank=True)
    featured = models.ForeignKey(
        'home.HomePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='features'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    
    def full_clean(self, *args, **kwargs):
        super(News, self).full_clean(*args, **kwargs)
        prefix = '{:%Y-%m-%d-}'.format(self.first_published_at) \
            if self.first_published_at \
            else '{:%Y-%m-%d-}'.format(datetime.now())

        if not self.slug.startswith(prefix):
            self.slug = prefix + self.slug
