from . base_importer import BaseImporter
from events.models import Event
from importer.models import Event as EventModel


class EventsImporter(BaseImporter):
    def execute(self):
        for data in self.export_query.get_all_data('node', 'event'):
            event = self.transform(data)
            self.listing.add_child(instance=event)

    def transform(self, data: dict):
        model = EventModel(data, self.export_query)

        event = Event(
            title=model.title,
            body=model.body,
            start_date=model.start_date,
            end_date=model.end_date,
        )

        return event
