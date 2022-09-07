from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel


class StaffMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job_title = blocks.CharBlock(required=False)
    email = blocks.EmailBlock(required=False)

    class Meta:
        icon = 'user'


class DepartmentListingPage(Page):
    """List departments."""

    template = "departments/departments_listing_page.html"
    max_count = 1
    subpage_types = ["staff_directory.DepartmentPage"]

    @property
    def get_child_pages(self):
        return DepartmentPage.objects.descendant_of(self).live()

    def get_sitemap_urls(self, request=None):
        return []


class DepartmentPage(Page):
    parent_page_types = ['staff_directory.DepartmentListingPage']
    staff = StreamField([
        ('staff_members', StaffMemberBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('staff', classname="full"),
    ]
