from django.core.management.base import BaseCommand, CommandParser
import os
import json
from pprint import pprint
from django.contrib.auth.models import User, Group, Permission, ContentType

import events.models
from ...importers.user_importer import transform_user
from ...importers.news_importer import NewsImporter
from ...importers.department_importer import DepartmentImporter
from ...importers.about_page_importer import AboutPageImporter
from ...importers.clubs_importer import ClubsImporter
from ...importers.events_importer import EventsImporter
from ...importers.home_importer import HomeImporter
from ...importers.menu_importer import MenuImporter
from ...importers.resources_importer import ResourcesImporter
from ...importers.advanced_pages_importer import AdvancedPagesImporter
from home.models import HomePage
from school_api.school_api import SchoolApi
from wagtail.models.sites import Site
from wagtail.models import GroupPagePermission, Collection, GroupCollectionPermission
from news.models import NewsListingPage
from events.models import EventListingPage
from staff_directory.models import DepartmentListingPage
from wagtail.core.models import Page
from ...query.file_query import FileQuery
from wagtail.core.blocks import StreamValue


class Command(BaseCommand):
    help = 'Import Drupal 7 HCPSS Schoolsite content from JSON files.'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.school_data = None
        self.directory = None
        self.acronym = None
        self.export_query = None

    def add_arguments(self, parser):
        parser: CommandParser
        parser.add_argument('acronym', type=str, help='The school acronym.')
        parser.add_argument('directory', type=str, help='The location of the export.')

    def create_structure(self):
        """Create site and root pages."""
        school_name = self.school_data['full_name']
        root = Page.get_first_root_node()

        home = HomePage(
            slug=self.acronym,
            title=school_name,
            show_in_menus=True,
        )
        root.add_child(instance=home)
        home.save()

        site = Site.objects.create(
            hostname="{acronym}.hcpss.localhost".format(acronym=self.acronym),
            root_page=home,
            is_default_site=False,
            site_name=school_name
        )
        site.save()

        event_listing = EventListingPage(slug="calendar", title="Latest Events", show_in_menus=True)
        home.add_child(instance=event_listing)
        event_listing.save()

        news_listing = NewsListingPage(slug="news", title="Latest News", show_in_menus=True)
        home.add_child(instance=news_listing)
        news_listing.save()

        directory = DepartmentListingPage(slug="school-staff", title="Directory Listing", show_in_menus=True)
        home.add_child(instance=directory)
        directory.save()

        return site, home, news_listing, event_listing, directory

    def import_users(self, group: Group):
        """Import users from json files."""
        for file in os.listdir(os.path.join(self.directory, 'user')):
            file_path = os.path.join(self.directory, 'user', file)
            username = file.split('__')[0]

            if not username or username == 'HCPSS Feed Importer':
                continue

            f = open(file_path)
            data = json.load(f)
            user = transform_user(data)
            user.groups.add(group)

    def import_menu(self, home: HomePage):
        """Import basic pages."""
        menu_data = self.export_query.get_data(prefix="main-menu")
        for item in menu_data:
            if item["link_path"].startswith("http"):
                continue

            data = self.export_query.find_by_path(item["link_path"])
            if data:
                if "admin_title" in data:
                    # This is an advanced page
                    print("Advanced page")
                elif "type" in data and data["type"] == "page":
                    # This is a basic page
                    print("Basic page")
                    #pprint(data)


    def handle(self, *args, **kwargs):
        self.acronym = kwargs['acronym']
        self.directory = kwargs['directory']
        self.school_data = SchoolApi(self.acronym).getData()
        self.export_query = FileQuery(self.directory)

        site, home, news_listing, event_listing, directory = self.create_structure()
        group = Group.objects.create(name=self.acronym.upper() + " Manager")

        collection = Collection(name=self.acronym.upper() + " Assets")
        Collection.get_first_root_node().add_child(instance=collection)

        content_type = ContentType.objects.get(model="document")
        for permission in content_type.permission_set.all():
            GroupCollectionPermission(group=group, collection=collection, permission=permission).save()

        GroupPagePermission(group=group, page=home, permission_type="add").save()
        GroupPagePermission(group=group, page=home, permission_type="edit").save()
        GroupPagePermission(group=group, page=home, permission_type="publish").save()
        GroupPagePermission(group=group, page=home, permission_type="bulk_delete").save()
        GroupPagePermission(group=group, page=home, permission_type="lock").save()
        GroupPagePermission(group=group, page=home, permission_type="unlock").save()

        self.import_users(group)

        importers = [
            NewsImporter(self.export_query, news_listing),
            EventsImporter(self.export_query, event_listing),
            ResourcesImporter(self.export_query, site),
            HomeImporter(self.export_query, home),
            DepartmentImporter(self.export_query, directory),
            AdvancedPagesImporter(self.export_query, home, "about"),
            ClubsImporter(self.export_query, home),
            AdvancedPagesImporter(self.export_query, home, "services"),
            AdvancedPagesImporter(self.export_query, home, "support"),
            AdvancedPagesImporter(self.export_query, home, "resources"),
            MenuImporter(self.export_query, site),
        ]

        for importer in importers:
            importer.execute()
