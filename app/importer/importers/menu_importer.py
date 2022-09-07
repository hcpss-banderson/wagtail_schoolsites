from .base_importer import BaseImporter
from menus.models import Menu, MenuItem
from django.utils.text import slugify
from wagtail.models import Page


class MenuImporter(BaseImporter):
    def execute(self):
        menu = Menu(title="Main", slug="main", site=self.listing)
        menu.save()

        menu_data = self.fetch_menu_data()

        items = dict()
        for mlid, item_data in menu_data.items():
            submenu = None
            item = MenuItem(link_title=item_data["link_title"], page=menu)

            if item_data["link_path"].startswith("http"):
                item.link_url = item_data["link_path"]
            else:
                slug_parts = item_data["link_path"].split("/")

                if slug_parts[0] == "node":
                    node_data = self.export_query.find_by_id("node", slug_parts[-1])
                    slug = node_data["alias"].split("/")[-1]
                else:
                    slug = slug_parts[-1]

                try:
                    if slug == "<front>":
                        page = self.listing.root_page
                    else:
                        page = Page.objects.descendant_of(self.listing.root_page).get(slug__exact=slug)
                    item.link_page = page
                except Page.DoesNotExist:
                    print("Not found: " + slug)

            if int(item_data["has_children"]):
                submenu = Menu(title=item_data["link_title"], slug=slugify(item_data["link_title"]), site=self.listing)
                submenu.save()
                item.title_of_submenu = submenu.title

            if int(item_data["plid"]):
                item.page = items[int(item_data["plid"])]["submenu"]

            item.save()
            items[mlid] = {"link": item, "submenu": submenu}

    def fetch_menu_data(self) -> dict:
        items: list = self.export_query.fetch("main-menu.json")
        items.sort(key=lambda m: (int(m["depth"]), int(m["weight"])))

        lookup = dict()
        for item in items:
            if int(item["hidden"]) == 0:
                lookup[int(item["mlid"])] = item

        return lookup
