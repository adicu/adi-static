import datetime as dt
import json
import os
import shutil
import string

import requests

SEMESTERS = {
    "2017F": (dt.date(2017, 9, 1), dt.date(2017, 12, 31)),
}

# Why do we even need an acess token for publicly available information?
ACCESS_TOKEN = "EAAMZA08pZBs7ABANfSAX2m1wsoB9s54iRWrOSMwNlS9H3waFrKsXraX9ZCjZBsABFndAyQCql8PO4xKMNzaZCpTij7KvhZAtpJmeo6IJF7qWDTPqWhZCZCOLIDEaPVJFIYR8UYqDeHUSVsvaRfkCBpkhZCN5tiZBkDJABkmQ2qrPmQtgZDZD"


def api(path, params=None):
    if params is None:
        params = {}
    params.update({"access_token": ACCESS_TOKEN})
    r = requests.get(
        "https://graph.facebook.com/v2.10/{}".format(path), params=params)
    return r.json()


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
        self.background_image = event["cover"]["source"]
        self.location = event["place"]["name"]

    @property
    def slug(self):
        s = "".join(char for char in self.title.lower()
                    if char in string.ascii_lowercase or char in " ")
        return s.replace(" ", "-").replace("--", "-")

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
            fout.write("background_image: " + self.background_image)
            fout.write("\n---\n")

            fout.write("short_description: " + self.short_description)
            fout.write("\n---\n")
            fout.write("long_description: " + self.long_description)


if __name__ == "__main__":
    events = api("adicu", {"fields": "events"})["events"]["data"]

    for event in events:
        event = Event(api(event["id"], {
            "fields": ",".join([
                "cover", "description", "start_time", "end_time", "name",
                "place", "id", "updated_time",
            ])
        }))  # yapf: disable
        event.write()
