from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from resources.models import ResourceList
from wagtail.fields import RichTextField
from wagtailimporter.serializer import GetOrCreateClusterableForeignObject
from wagtail.contrib.settings.models import BaseSetting, register_setting

import resources.models


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(help_text="Your Facebook URL", blank=True)
    instagram = models.CharField(max_length=255, help_text="Your Instagram username, without the @", blank=True)

    panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
    ]

    class Meta:
        verbose_name = "Social Media Accounts"


class HomePage(Page):
    resource_list_one = models.ForeignKey(ResourceList, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    resource_list_two = models.ForeignKey(ResourceList, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    resource_list_three = models.ForeignKey(ResourceList, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    content_panels = Page.content_panels + [
        InlinePanel("featured_content", label="Featured Content", max_num=9),
        MultiFieldPanel([
            FieldPanel("resource_list_one"),
            FieldPanel("resource_list_two"),
            FieldPanel("resource_list_three"),
        ], heading="Resource Lists"),
    ]

    # class Meta:
    #     unique_together = (
    #         ()
    #     )


class Feature(Page):
    body = RichTextField(blank=True, null=True)


class FeaturedContent(Orderable):
    max_count = 9

    page = ParentalKey("home.HomePage", related_name='featured_content')
    content = models.ForeignKey('home.Feature', related_name="+", on_delete=models.CASCADE)

    panels = [
        FieldPanel("content")
    ]


class RelatedFeatureTag(GetOrCreateClusterableForeignObject):
    model = Feature
    yaml_tag = '!relatedfeature'
    lookup_keys = ('url_path',)

    def get_object(self):
        model = super().get_object()
        model.save()
        return model


class RelatedFeatureContentTag(GetOrCreateClusterableForeignObject):
    model = FeaturedContent
    yaml_tag = '!relatedfeaturecontent'
    lookup_keys = ('content',)

    def get_object(self):
        model = super().get_object()
        model.save()
        return model
