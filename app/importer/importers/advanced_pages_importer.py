from . base_importer import BaseImporter
from importer.models import StaffMember, PageSection
from ..query.file_query import FileQuery
from wagtail.core.models import Page
from advanced_pages.models import AdvancedPage
from wagtail.core.blocks import StreamValue


class AdvancedPagesImporter(BaseImporter):
    def __init__(self, export_query: FileQuery, listing: Page, slug: str):
        super().__init__(export_query, listing)
        self.data = self.export_query.find_by_path(slug)
        self.slug = slug

    def execute(self):
        title = self.data["title"] if "title" in self.data else self.data["display"]["title"]
        page = AdvancedPage(title=title, slug=self.slug)
        stream = self.get_stream_from_node() if "nid" in self.data else self.get_stream_from_panel()
        page.body = StreamValue('staff', stream, True)
        self.listing.add_child(instance=page)

    def get_stream_from_panel(self):
        stream = []
        for pane in self.data["panes"]:
            if pane["shown"] != "1":
                continue

            if pane["type"] == "node":
                # This is a node
                node_data = self.export_query.find_by_id("node", pane["configuration"]["nid"])
                if not node_data:
                    continue

                match node_data["type"]:
                    case "school_staff_member":
                        m = StaffMember(node_data, self.export_query)
                        member = {
                            "type": "staff",
                            "value": {
                                "name": m.name,
                                "job_title": m.job_title,
                                "email": m.email,
                                "biography": m.biography,
                                "photo": m.photo
                            }
                        }
                        stream.append(member)
                    case "page_section":
                        s = PageSection(node_data, self.export_query)
                        section = {
                            "type": "paragraph",
                            "value": s.body
                        }
                        stream.append(section)

        return stream

    def get_stream_from_node(self, data: dict):
        stream = []

        try:
            body = {
                "type": "paragraph",
                "value": self.data['body']['und'][0]['value'],
            }
            stream.append(body)
        except KeyError:
            pass

        return stream