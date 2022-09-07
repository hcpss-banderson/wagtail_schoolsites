from . base_importer import BaseImporter
from staff_directory.models import DepartmentPage
from wagtail.core.blocks import StreamValue
from pprint import pprint
from programs.models import ProgramPage, ProgramListingPage
from importer.models import StaffMember


class ClubsImporter(BaseImporter):
    def execute(self):
        listing_data = self.export_query.get_all_data('node', 'club')
        if not len(listing_data):
            return

        program_listing = ProgramListingPage(slug="clubs", title="Clubs and Honor Societies")
        self.listing.add_child(instance=program_listing)
        program_listing.save()

        for program_data in listing_data:
            program = self.transform(program_data)
            program_listing.add_child(instance=program)

    def transform(self, data: dict):
        advisors = []
        try:
            for target in data["field_coach"]:
                member = self.export_query.get_data('node', "school_staff_member", target["target_id"])
                if member:
                    model = StaffMember(member)
                    advisors.append({
                        "type": "staff_list",
                        "value": {
                            "name": model.name,
                            "job_title": model.job_title,
                            "email": model.email,
                        }
                    })
        except (KeyError, TypeError):
            pass

        program = ProgramPage(title=data["title"], slug=data["alias"].split("/")[-1], staff_role="Advisors")
        program.staff = StreamValue('staff', advisors, True)

        try:
            program.body = data["body"]["und"][0]["value"]
        except (KeyError, TypeError):
            pass

        return program
