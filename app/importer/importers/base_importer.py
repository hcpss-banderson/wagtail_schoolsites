from ..query.file_query import FileQuery
from wagtail.core.models import Page


class BaseImporter:
    def __init__(self, export_query: FileQuery, listing: Page):
        self.export_query = export_query
        self.listing = listing

    def execute(self, data: dict):
        pass
