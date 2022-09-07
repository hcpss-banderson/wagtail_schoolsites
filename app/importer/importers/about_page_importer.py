from news.models import News
from advanced_pages.models import AdvancedPage
from . advanced_pages_importer import AdvancedPagesImporter
from wagtail.core.blocks import StreamValue


class AboutPageImporter(AdvancedPagesImporter):
    def execute(self):
        page = AdvancedPage(title="About Us", slug="about")
        data = self.export_query.find_by_path("about")
        stream = self.get_stream_from_node(data) if "nid" in data else self.get_stream_from_panel(data)
        page.body = StreamValue('staff', stream, True)
        self.listing.add_child(instance=page)

    @staticmethod
    def transform(data: dict):
        news = News(
            title=data['title'],
            body=data['field_news_message_content']['und'][0]['value'],
        )

        return news
