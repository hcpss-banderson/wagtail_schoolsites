from . base_importer import BaseImporter
from news.models import News
from home.models import HomePage, Feature, FeaturedContent
from resources.models import Resource, ResourceList
from pprint import pprint
from wagtail.models.sites import Site


class HomeImporter(BaseImporter):
    def execute(self):
        highlight_data = self.export_query.get_all_data("node", "homepage_highlights").pop()
        self.highlights(highlight_data)

        self.resources()
        self.listing.save()

    def resources(self):
        site = Site.objects.get(root_page=self.listing)

        list_one = ResourceList.objects.get(site=site, title="Essential Applications")
        self.listing.resource_list_one = list_one

        list_two = ResourceList.objects.get(site=site, title="HCPSS Resources")
        self.listing.resource_list_two = list_two

        list_three = ResourceList.objects.get(site=site, title="Get Involved")
        self.listing.resource_list_three = list_three

    def highlights(self, data: dict):
        page = self.listing

        for target in data["field_highlighted_items"]["und"]:
            highlight_data = self.export_query.find_by_id("node", target["target_id"])

            if not highlight_data:
                continue

            feature = Feature.objects.filter(title__exact=highlight_data["title"]).first()

            if feature:
                relationship = FeaturedContent(page=page, content=feature)
                relationship.save()
