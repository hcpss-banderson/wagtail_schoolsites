from . base_importer import BaseImporter
from staff_directory.models import DepartmentPage
from wagtail.core.blocks import StreamValue
from pprint import pprint


class DepartmentImporter(BaseImporter):
    def execute(self):
        listing_data = self.export_query.get_all_data('node', 'school_staff_list').pop()

        for dep_target in listing_data['field_department_listing']['und']:
            department_data = self.export_query.get_data("node", "department", dep_target['target_id'])

            if not department_data:
                continue

            department = self.transform(department_data)
            self.listing.add_child(instance=department)

    def transform(self, data: dict):
        members = []
        for target in data['field_department_staff']['und']:
            staff_data = self.export_query.get_data('node', 'school_staff_member', target['target_id'])

            if not staff_data:
                continue

            try:
                job_title = staff_data['field_staff_job_title']['und'][0]['value']
            except Exception:
                job_title = ""

            try:
                email = staff_data['field_staff_email']['und'][0]['value']
            except Exception:
                email = ""

            members.append({
                "type": "staff_members",
                "value": {
                    "name": staff_data['title'],
                    "job_title": job_title,
                    "email": email,
                }
            })

        department = DepartmentPage(title=data['title'])
        department.staff = StreamValue('staff_members', members, True)

        return department
