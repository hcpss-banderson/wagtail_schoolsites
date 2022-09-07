import datetime
import io
import os.path
import re
import json
import willow
import requests
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from pprint import pprint
from importer.query.file_query import FileQuery
from datetime import datetime
import pytz


class BaseModel:
    def __init__(self, data: dict, export_query: FileQuery):
        self.export_query = export_query

    def fetch_image(self, fid: int, width: int, height: int, title: str) -> Image:
        img_data = self.export_query.find_by_id('file_info', fid)
        img_path = os.path.join(self.export_query.directory, 'files', img_data['uri'].split('/')[-1])
        img_file = ImageFile(open(img_path, 'rb'), name=img_data['filename'])

        image = Image(
            title=title,
            file=img_file,
            width=width,
            height=height,
            uploaded_by_user_id=1,
            file_size=img_file.size
        )
        image.save()

        # Force hash creation.
        image.get_file_hash()
        return image


class Resource(BaseModel):
    def __init__(self, data: dict, export_query: FileQuery):
        super().__init__(data, export_query)
        self.name = data["title"]
        self.url = data["field_link__url"]["und"][0]["url"]

        try:
            self.description = data["field_link_description"]["und"][0]["value"]
        except (KeyError, TypeError):
            self.description = None


class Event(BaseModel):
    def __init__(self, data: dict, export_query: FileQuery):
        super().__init__(data, export_query)
        self.title = data["title"]
        tz = pytz.timezone("America/New_York")

        try:
            self.body = data["body"]["und"][0]["value"]
        except (KeyError, TypeError):
            self.body = None

        try:
            start = data["field_event_date"]["und"][0]["value"]
        except (KeyError, TypeError):
            start = None

        try:
            end = data["field_event_date"]["und"][0]["value2"]
        except (KeyError, TypeError):
            end = None

        if end and not start:
            start = end
        if start and not end:
            end = start

        if start and end:
            naive_start = datetime.fromisoformat(start)
            naive_end = datetime.fromisoformat(end)

            self.start_date = tz.localize(naive_start)
            self.end_date = tz.localize(naive_end)
        else:
            self.start_date = datetime.now(tz=tz)
            self.end_date = datetime.now(tz=tz)



class StaffMember(BaseModel):
    def __init__(self, data: dict, export_query: FileQuery):
        super().__init__(data, export_query)
        self.name = data["title"]
        try:
            self.job_title = data['field_staff_job_title']['und'][0]['value']
        except KeyError:
            self.job_title = None

        try:
            self.email = data['field_staff_email']['und'][0]['value']
        except (KeyError, TypeError):
            self.email = None

        try:
            self.biography = data['body']['und'][0]['value']
        except (KeyError, TypeError):
            self.biography = None

        try:
            image = self.fetch_image(
                data["field_staff_photo"]['und'][0]['fid'],
                data["field_staff_photo"]['und'][0]['width'],
                data["field_staff_photo"]['und'][0]['height'],
                data["field_staff_photo"]['und'][0]['field_file_image_alt_text']['und'][0]['value']
            )
            self.photo = image.id
        except (KeyError, TypeError) as Error:
            self.photo = None


class PageSection(BaseModel):
    def __init__(self, data: dict, export_query: FileQuery):
        super().__init__(data, export_query)
        self.body = "<h2>{}</h2>".format(data["title"])

        try:
            body: str = data['body']['und'][0]['value']
            for media in re.findall('\[\[(.*)\]\]', body):
                media_data = json.loads(media)
                image = self.fetch_image(
                    media_data["fid"],
                    media_data["attributes"]["width"],
                    media_data["attributes"]["height"],
                    media_data["attributes"]["title"]
                )

                embed = '<embed alt="{alt}" embedtype="image" format="left" id="{id}" />'.format(
                    alt=image.title,
                    id=image.id
                )

                body = body.replace("[[{}]]".format(media), embed)

            self.body += body
        except (KeyError, TypeError) as Error:
            raise Error
