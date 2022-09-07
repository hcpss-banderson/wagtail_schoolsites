import json
import os
from pprint import pprint


class FileQuery():
    def __init__(self, directory: str):
        self.directory = directory

    def get_panes_by_display_id(self, display_id: int) -> dict:
        panels = []
        for file in os.listdir(os.path.join(self.directory, 'panels_pane')):
            if file.endswith("__{}.json".format(display_id)):
                panels.append(json.load(open(os.path.join(self.directory, "panels_pane", file))))

        return panels

    def get_manager_handler_by_name(self, name: str) -> dict:
        for handler_filename in self.list("page_manager_handlers"):
            handler_path = os.path.join(self.directory, "page_manager_handlers", handler_filename)
            manager = json.load(open(handler_path))
            if manager["subtask"] == name:
                return manager

        raise Exception("Handler {} not found.".format(name))

    def get_display_by_display_id(self, display_id: int) -> dict:
        display_filename = "{}.json".format(display_id)
        display_file = open(os.path.join(self.directory, "panels_display", display_filename))

        return json.load(display_file)

    def find_by_path(self, path: str):
        for page_file in self.list("page_manager_pages"):
            page_path = os.path.join(self.directory, "page_manager_pages", page_file)
            manager_page = json.load(open(page_path))
            if path == manager_page["path"]:
                manager_handler = self.get_manager_handler_by_name(manager_page["name"])
                display = self.get_display_by_display_id(manager_handler["did"])
                panes = self.get_panes_by_display_id(manager_page["pid"])

                return {
                    "manager_page": manager_page,
                    "manager_handler": manager_handler,
                    "display": display,
                    "panes": panes
                }

        for node_file in self.list("node"):
            file_path = os.path.join(self.directory, 'node', node_file)
            node_data = json.load(open(file_path))

            if path == node_data["alias"]:
                return node_data

        return None

    def find_by_id(self, entity_type: str, id: int):
        for file in self.list(entity_type):
            if file.endswith("__" + id + ".json") or file == id + ".json":
                path = os.path.join(self.directory, entity_type, file)
                return json.load(open(path))

        return None

    def list(self, entity_type: str = None):
        return os.listdir(os.path.join(self.directory, entity_type))

    def get_all_data(self, sub_directory: str=None, prefix: str=None) -> list:
        data = []
        dir = self.directory

        if sub_directory:
            dir = os.path.join(dir, sub_directory)

        for file in os.listdir(dir):
            if not prefix or file.startswith(prefix):
                data.append(json.load(open(os.path.join(dir, file))))

        return data

    def fetch(self, path: str):
        if os.path.exists(os.path.join(self.directory, path)):
            f = open(os.path.join(self.directory, path))
            data = json.load(f)
            return data

        # If we found the file we would not be here.
        return None

    def get_data(self, sub_directory: str, prefix: str, id: int):
        dir_parts = []
        if sub_directory:
            dir_parts.append(sub_directory)

        file_parts = []
        if prefix:
            file_parts.append(prefix)

        if id:
            file_parts.append(id)

        filename = "__".join(file_parts) + ".json"
        dir_parts.append(filename)
        candidate = os.path.join(*dir_parts)
        return self.fetch(path=candidate)
