# -*- coding: utf-8 -*-
import datetime as dt

from lektor.pluginsystem import Plugin
from lektor.project import Project


class FakeQuery(object):
    def __init__(self, data, limit=None):
        self.data = data
        if limit:
            self.data = self.data[:limit]
    def count(self):
        return len(self.data)
    def all(self):
        return self.data
    def first(self):
        if self.data:
            return self.data[0]
    def __iter__(self):
        return iter(self.data)
    def limit(self, limit):
        return FakeQuery(self.data, limit)
    def offset(self, offset):
        return FakeQuery(self.data[offset:])


class EventsPlugin(Plugin):
    name = u'events'
    description = u'Add events to globally Jinja2 templates'

    def on_setup_env(self, **extra):
        pad = self.env.new_pad()
        now = dt.datetime.now()

        upcoming = []
        past = []
        stack = [pad.root]

        while stack:
            for child in stack.pop().children:
                if child["_model"] == "event":
                    if child["end"] > now:
                        upcoming.append(child)
                    else:
                        past.append(child)
                else:
                    stack.append(child)

        past = sorted(past, key=lambda x: x["start"], reverse=True)
        upcoming = sorted(upcoming, key=lambda x: x["start"])

        self.env.jinja_env.globals["past_events"] = FakeQuery(past)
        self.env.jinja_env.globals["upcoming_events"] = FakeQuery(upcoming)
