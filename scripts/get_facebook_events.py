import datetime as dt
import os
import shutil
import string
import urllib

import requests

SEMESTERS = {
    "2017F": (dt.date(2017, 9, 1), dt.date(2017, 12, 31)),
    "2018S": (dt.date(2018, 1, 1), dt.date(2018, 5, 31)),
    "2018F": (dt.date(2018, 9, 1), dt.date(2018, 12, 31)),
    "2019S": (dt.date(2019, 1, 1), dt.date(2019, 5, 31)),
    "2019F": (dt.date(2019, 9, 1), dt.date(2019, 12, 31)),
}

# Why do we even need an acess token for publicly available information?
# See https://medium.com/@Jenananthan/how-to-create-non-expiry-facebook-page-token-6505c642d0b1
# and https://developers.facebook.com/tools/accesstoken/
ACCESS_TOKEN = "EAAF61ek8o5cBAMIJyoQUn12BITFxC1mb2p0JmTRkszQ6wXOC5woxLwRwlXvLHKhwXPsaFBXaiAAmEtyZAgnhc0tXpA6WJ7M8t0seX0jnj18WCoFULeetN1Jpde3YUGj4EdT8K4vneFH02sp0HboQOhrdIETJuk9hzUJ8aSAZDZD"


def api(path, params=None):
    if params is None:
        params = {}
    params.update({"access_token": ACCESS_TOKEN})
    r = requests.get(
        "https://graph.facebook.com/v2.12/{}".format(path), params=params)
    return r.json()

def image_api(path):
    r = requests.get(path, stream=True)
    return r.raw

def parse_iso8601(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def write_lektor_datetime(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M")


class Event(object):
    def __init__(self, event):
        self.start = parse_iso8601(event["start_time"])
        self.end = parse_iso8601(event["end_time"])
        self.last_updated = parse_iso8601(event["updated_time"])

        self.title = event["name"].strip()
        self.long_description = event["description"].strip().replace(
            "---", "----")
        self.short_description = self.long_description.split("\n")[0]

        self.facebook_url = "https://facebook.com/events/" + event['id']
        self.background_image = None

        if "cover" in event:
            self.background_image = image_api(event["cover"]["source"])
        try:
            self.location = event["place"]["name"]
        except KeyError:
            self.location = ""

    @property
    def slug(self):
        date = self.start.strftime("%Y-%m-%d")
        s = "".join(char for char in self.title.lower()
                    if char in string.ascii_lowercase or char in " ")
        return date + "-" + s.replace(" ", "-").replace("--", "-")

    @property
    def path(self):
        root = self.root()
        if root is not None:
            return os.path.join(root, self.slug)

    def root(self):
        root = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../content/events")
        for key, (start, end) in SEMESTERS.items():
            if start <= self.start.date() <= end:
                return os.path.join(root, key)

    def write(self):
        if not self.path:
            return

        # delete old event
        root = self.root()
        os.makedirs(root, exist_ok=True)
        for d in os.listdir(root):
            d = os.path.join(root, d)
            if not os.path.isdir(d):
                continue
            with open(os.path.join(d, "contents.lr")) as fin:
                parts = fin.read().split('\n---\n')
            if any(part == "facebook_url: " + self.facebook_url
                   for part in parts):
                shutil.rmtree(os.path.join(d))

        # create new event
        os.makedirs(self.path)
        with open(os.path.join(self.path, "contents.lr"), "w") as fout:
            fout.write("_model: event")
            fout.write("\n---\n")
            fout.write("title: " + self.title)
            fout.write("\n---\n")
            fout.write("start: " + write_lektor_datetime(self.start))
            fout.write("\n---\n")
            fout.write("end: " + write_lektor_datetime(self.end))
            fout.write("\n---\n")

            fout.write("facebook_url: " + self.facebook_url)
            fout.write("\n---\n")
            fout.write("location: " + self.location)
            fout.write("\n---\n")
            if self.background_image is not None:
                fout.write("background_image: " + "cover.jpg")
                fout.write("\n---\n")

            fout.write("short_description: " + self.short_description)
            fout.write("\n---\n")
            fout.write("long_description: " + self.long_description)

        if self.background_image is not None:
            with open(os.path.join(self.path, "cover.jpg"), "wb") as fout:
                shutil.copyfileobj(self.background_image, fout)

if __name__ == "__main__":
    response = api("adicu", {"fields": "events"})
    try:
        events = response['events']['data']
    except KeyError:
        raise ValueError("{}".format(response))

    for event in events:
        event = Event(api(event["id"], {
            "fields": ",".join([
                "cover", "description", "start_time", "end_time", "name",
                "place", "id", "updated_time",
            ])
        }))  # yapf: disable
        event.write()
