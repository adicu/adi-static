import datetime as dt
import json
import os
import string

import requests

SEMESTERS = {
    "2017F": (dt.date(2017, 9, 1), dt.date(2017, 12, 31)),
}

# Why do we even need an acess token for publicly available information?
ACCESS_TOKEN = "EAACEdEose0cBAKUe6mnfZCW1acmWp03WLFhHUIzVQiuR8oKNz1yISyVGqAjh5eYSTr2W3p09BWh5n5ZAOWoNfKrk1IV1ZBVZCpFsb9gqEQZASQ8E595mKCKVZBOUU5vV7INS11qQco89uyKrMSouAeA7I2gEY6EusF8GRkXP7ddJE7jdbq6X3D4Por9QSDOYZCbGT3tpEpdqQZDZD"


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
        root = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../content/events")
        for key, (start, end) in SEMESTERS.items():
            if start <= self.start.date() <= end:
                return "{}/{}/{}/".format(root, key, self.slug)

    def write(self):
        if not self.path:
            return
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        with open(self.path + "contents.lr", "w") as fout:
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
