import requests
import yaml
from pprint import pprint


class debrid:

    def __init__(self, config) -> None:
        self.url_base = "https://api.real-debrid.com/rest/1.0/"
        self.api_key = config["api_key"]
        self.

    def request(self, url, type, body=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if type == "GET":
            response = requests.get(url, headers=headers)
            return response.json()

    def get_current_torrents(self):
        url = f"{self.url_base}/torrents"

        response = self.request(url, type="GET")

        pprint(response)

    def get_torrent_hash(self, filename):
        pass

    def get_instant_availability(self, hash):
        url = f"{self.url_base}/torrents/instantAvailability/{hash}"


if __name__ == "__main__":

    with open("config.yml") as f:
        config = yaml.safe_load(f)

    service = debrid(api_key=config)
    service.get_current_torrents()
