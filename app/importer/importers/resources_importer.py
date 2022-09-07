from .base_importer import BaseImporter
from resources.models import Resource, ResourceList


class ResourcesImporter(BaseImporter):
    def execute(self):
        lists_data: list = self.export_query.fetch("essential_applications_and_resources.json")

        for list_data in lists_data:
            match list_data["menu"]:
                case "Essential Applications":
                    icon = "location-dot"
                case "Get Involved":
                    icon = "handshake-angle"
                case _:
                    icon = "badge"

            resource_list = ResourceList(title=list_data["menu"], site=self.listing, icon=icon)
            resource_list.save()

            for resource_data in list_data["resources"]:
                resource = Resource(
                    title=resource_data["name"],
                    url=resource_data["href"],
                    description=resource_data["description"],
                    list=resource_list
                )
                resource.save()


