import requests
import yaml
from pprint import pprint
import re


class debrid:

    def __init__(self, config) -> None:
        self.url_base = "https://api.real-debrid.com/rest/1.0/"
        self.api_key = config["api_key"]
        self.sonarr_watch_folder = config["sonarr_blackhole_dir"]
        self.radarr_watch_folder = config["radarr_blackhole_dir"]

    def request(self, url, type, body=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if type == "GET":
            response = requests.get(url, headers=headers)

        if type == "POST":
            response = requests.post(url, headers=headers, data=body)
        return response.json()

    def get_current_torrents(self):
        url = f"{self.url_base}/torrents"

        response = self.request(url, type="GET")

        pprint(response)

    def get_torrent_hash(self, filename, isRadarr=True):

        with open(filename) as t:
            torrent = t.read()
        p = re.search("btih:(.*)&dn", torrent)
        magnet_hash = p.group(1)

        compiled = {"hash": magnet_hash, "magnet": torrent}

        return compiled

    def get_instant_availability(self, hash=None):
        url = f"{self.url_base}/torrents/instantAvailability/{hash}"

        response = self.request(url, type="GET")

    def download_magnet(self, magnet):

        url = f"{self.url_base}/torrents/addMagnet"

        body = {"magnet": magnet["magnet"]}
        response = self.request(url, type="POST", body=body)
        url = response["uri"]
        response = self.request(url, type="GET")

        pprint(response)


if __name__ == "__main__":

    with open("config.yml") as f:
        config = yaml.safe_load(f)

    config["radarr_blackhole_dir"] = "tests/torrents"
    config["sonarr_blackhole_dir"] = "test/torrents"
    service = debrid(config)
    torrent = service.get_torrent_hash(
        "Dune.2021.2160p.BluRay.REMUX.HEVC.DTS-HD.MA.TrueHD.7.1.Atmos-FGT.magnet"
    )

    service.download_magnet(torrent)
