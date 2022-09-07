from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from staff_directory.models import StaffMemberBlock
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


class ProgramPage(Page):
    body = RichTextField(blank=True, null=True)
    staff = StreamField([('staff_list', blocks.ListBlock(StaffMemberBlock()))], use_json_field=True)
    staff_role = models.CharField(blank=True, max_length=100, help_text='"Coaches", "Advisors", "Sponsors", etc.')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class ProgramListingPage(Page):
    """List programs."""

    template = "programs/programs_listing_page.html"
    subpage_types = ["programs.ProgramPage"]
    parent_page_types = ['home.HomePage']

    @property
    def get_child_pages(self):
        return ProgramPage.objects.descendant_of(self).live()

    def get_sitemap_urls(self, request=None):
        return []
