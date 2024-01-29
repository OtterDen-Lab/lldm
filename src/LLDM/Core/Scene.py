import networkx as nx

from LLDM.Core.Map import Map
from LLDM.Utility.PrettyPrinter import NestedFormatter


class Event:
    """
    Events are the descriptions of actions or reactions created through play.
    User inputs are processed by GPT into action Events, then resolved by GPT again to produce reaction Events
    """
    def __init__(self, title: str, summary: str, category: str):
        self._title = title
        self._summary = summary
        self._category = category

    def __str__(self):
        return f"[{self.category}] {self.title}: {self.summary}"

    def __repr__(self):
        return f"[{self.category}] {self.title}: {self.summary}"

    @property
    def summary(self):
        return self._summary

    @property
    def title(self):
        return self._title

    @property
    def category(self):
        return self._category

    @title.setter
    def title(self, value: str):
        self._title = value

    @summary.setter
    def summary(self, value: str):
        self._summary = value


class Scene(NestedFormatter):
    """
    Scene represent the top level object.
    It holds the entire map/graph data, all events that have occurred, and all characters present.
    """
    time = 0

    def __init__(self, loc_map, events=None):
        self._loc_map = loc_map
        self._events = events if events is not None else []

    @property
    def loc_map(self):
        return self._loc_map

    @loc_map.setter
    def loc_map(self, loc_map: Map):
        self._loc_map = loc_map

    @property
    def events(self):
        return self._events

    def add_event(self, event: Event):
        self._events.append(event)
