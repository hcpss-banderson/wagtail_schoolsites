from base_importer import BaseImporter
from basic_pages.models import BasicPage


class PageImporter(NodeImporter):
    def execute(self):
        for data in self.export_query.get_data('node', 'news_message'):
            news = self.transform(data)
            self.listing.add_child(instance=news)

    def transform(self, data: dict):
        news = News(
            title=data['title'],
            body=data['field_news_message_content']['und'][0]['value'],
        )

        return news
