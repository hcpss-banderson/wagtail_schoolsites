from django.db import models
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from staff_directory.models import StaffMemberBlock


class LatestNewsStaticBlock(blocks.StaticBlock):
    class Meta:
        icon = 'list-ul'
        label = 'Latest news'
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'news_posts.html'


class StaffMemberFeatureBlock(StaffMemberBlock):
    biography = blocks.RichTextBlock(required=False)
    photo = ImageChooserBlock(required=False)


class ResourceBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    url = blocks.URLBlock()
    description = blocks.CharBlock()


class HeadingBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(choices=[
        ('h2', 'Heading 2'),
        ('h3', 'Heading 3'),
        ('h4', 'Heading 4'),
        ('h5', 'Heading 5'),
        ('h6', 'Heading 6'),
    ])
    title = blocks.CharBlock()


class ResourceListBlock(blocks.StructBlock):
    resources = ResourceBlock()


class AdvancedPage(Page):
    template = "advanced_page/show.html"

    body = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('staff', StaffMemberFeatureBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
