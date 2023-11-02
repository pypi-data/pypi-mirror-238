import time
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from io import StringIO
from typing import Any

import feedparser  # type: ignore
import requests


class MLStripper(HTMLParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data: str) -> None:
        self.text.write(data)

    def strip_tags(self, html: str) -> str:
        self.feed(unescape(html))
        text = self.text.getvalue()
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())


@dataclass
class Entry:
    id: str
    feed_url: str
    title: str
    link: str
    description: str = ""
    published_timestamp: int = 0
    published: time.struct_time | None = None

    def __post_init__(self) -> None:
        self.title = unescape(self.title)
        self.description = MLStripper().strip_tags(self.description)
        if self.published is not None:
            self.published_timestamp = int(time.mktime(self.published))


@dataclass
class Feed:
    url: str = ""
    update_interval: int = 1800
    enabled: bool = True
    last_updated: int = 0
    title: str = ""
    notify_with_guid: bool = False

    def __post_init__(self) -> None:
        self.enabled = bool(self.enabled)

    def parse(self) -> feedparser.util.FeedParserDict | None:
        try:
            with requests.get(self.url, timeout=15.0) as r:
                return feedparser.api.parse(r.text)  # type: ignore
        except requests.RequestException:
            return None

    def get_entries(self) -> list[Entry]:
        d = self.parse()
        if d is None:
            return []
        self.title = d.feed.title  # type: ignore
        entries = d.entries  # type: ignore
        return [
            Entry(
                id=entry.id,  # type: ignore
                feed_url=self.url,
                title=entry.title,  # type: ignore
                link=entry.link,  # type: ignore
                description=entry.description,  # type: ignore
                published=entry.published_parsed,  # type: ignore
            )
            for entry in entries  # type: ignore
        ]
