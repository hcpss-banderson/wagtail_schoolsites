import requests
from pprint import pprint

class SchoolApi:
    def __init__(self, acronym):
        self.acronym = acronym

    def getData(self):
        url = "https://api.hocoschools.org/schools/" + self.acronym + ".json"
        r = requests.get(url)
        return r.json()
