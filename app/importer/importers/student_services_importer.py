from . base_importer import BaseImporter
from news.models import News
from pprint import pprint
from advanced_pages.models import AdvancedPage, StaffMemberFeatureBlock
from importer.models import StaffMember, PageSection
from wagtail.core.blocks import StreamValue


class StudentServicesImporter(BaseImporter):

    def execute(self):
        data = self.export_query.find_by_path("student-services")
        if not data:
            data = self.export_query.find_by_path("student-services/overview")

        if not data:
            return

        page = AdvancedPage(title="Student Services", slug="student-services")
        panels  = []
        for pane in data["panels"]:
            panels.append(self.transform(pane))

        page.body = StreamValue('staff', panes, True)
        self.listing.add_child(instance=page)




        # page = AdvancedPage(title="About Us", slug="about")
        # data = self.export_query.find_by_path("about")
        # stream = self.get_stream_from_node(data) if "nid" in data else self.get_stream_from_panel(data)
        # page.body = StreamValue('staff', stream, True)
        # self.listing.add_child(instance=page)

    def transform(self, data: dict):
        news = News(
            title=data['title'],
            body=data['field_news_message_content']['und'][0]['value'],
        )

        return news


    # def get_stream_from_panel(self, data: dict):
    #     stream = []
    #     for pane in data["panes"]:
    #         if pane["shown"] != "1":
    #             continue
    #
    #         if pane["type"] == "node":
    #             # This is a node
    #             node_data = self.export_query.find_by_id("node", pane["configuration"]["nid"])
    #             if not node_data:
    #                 continue
    #
    #             match node_data["type"]:
    #                 case "school_staff_member":
    #                     m = StaffMember(node_data, self.export_query)
    #                     member = {
    #                         "type": "staff",
    #                         "value": {
    #                             "name": m.name,
    #                             "job_title": m.job_title,
    #                             "email": m.email,
    #                             "biography": m.biography,
    #                             "photo": m.photo
    #                         }
    #                     }
    #                     stream.append(member)
    #                 case "page_section":
    #                     s = PageSection(node_data, self.export_query)
    #                     section = {
    #                         "type": "paragraph",
    #                         "value": s.body
    #                     }
    #                     stream.append(section)
    #
    #     return stream
    #
    # def get_stream_from_node(self, data: dict):
    #     stream = []
    #
    #     try:
    #         body = {
    #             "type": "paragraph",
    #             "value": data['body']['und'][0]['value'],
    #         }
    #         stream.append(body)
    #     except KeyError:
    #         pass
    #
    #     return stream