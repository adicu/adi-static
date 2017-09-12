# -*- coding: utf-8 -*-
import datetime as dt

from lektor.pluginsystem import Plugin
from lektor.project import Project


class FakeQuery(object):
    def __init__(self, data, *args, **kwargs):
        self._data = data
        self._limit = kwargs.pop("limit", None)
        self._offset= kwargs.pop("offset", 0)

        assert len(args) == 0
        assert len(kwargs) == 0

    @property
    def data(self):
        if self._limit:
            return self._data[self._offset: self._offset + self._limit]
        return self._data[self._offset:]
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
        return FakeQuery(self._data, limit=limit, offset=self._offset)
    def offset(self, offset):
        return FakeQuery(self._data, limit=self._limit, offset=offset)


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
