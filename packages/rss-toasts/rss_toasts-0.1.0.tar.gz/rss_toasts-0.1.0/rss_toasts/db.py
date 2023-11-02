import os
import sqlite3
from types import TracebackType
from typing import Self

import platformdirs

from rss_toasts.feed import Entry, Feed


class Database:
    def __init__(self):
        db_dir = platformdirs.user_data_dir(
            "rss-toasts", appauthor=False, roaming=True, ensure_exists=True
        )
        self.db_file = os.path.join(db_dir, "database.db")
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.migrate()

    def close(self):
        self.conn.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        self.close()

    def migrate(self):
        version = int(
            self.conn.execute("PRAGMA user_version").fetchone()["user_version"]
        )
        if version == 0:
            with self.conn as c:
                c.execute(
                    """
                    CREATE TABLE IF NOT EXISTS feeds (
                        url TEXT NOT NULL UNIQUE,
                        update_interval INTEGER NOT NULL,
                        enabled INTEGER NOT NULL,
                        last_updated INTEGER NOT NULL,
                        notify_with_guid INTEGER NOT NULL
                    );
                    """
                )
                c.execute(
                    """
                    CREATE TABLE IF NOT EXISTS entries (
                          id TEXT UNIQUE,
                          feed_url INTEGER NOT NULL,
                          title TEXT NOT NULL,
                          link TEXT NOT NULL,
                          published_timestamp INTEGER NOT NULL,
                          FOREIGN KEY(feed_url) REFERENCES feeds(url)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
                    )
                    """
                )
                c.execute("PRAGMA user_version = 1")

    def get_feeds(self) -> list[Feed]:
        return [Feed(**row) for row in self.conn.execute("SELECT * FROM feeds")]

    def add_feed(self, feed: Feed) -> bool:
        try:
            with self.conn as c:
                c.execute(
                    """
                    INSERT INTO feeds (
                        url, update_interval, enabled, last_updated, notify_with_guid
                    ) VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        feed.url,
                        feed.update_interval,
                        feed.enabled,
                        feed.last_updated,
                        feed.notify_with_guid,
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def update_feed(self, feed: Feed):
        with self.conn as c:
            c.execute(
                """
                UPDATE feeds SET
                    url = ?, update_interval = ?, enabled = ?, last_updated = ?,
                    notify_with_guid = ?
                WHERE url = ?;
                """,
                (
                    feed.url,
                    feed.update_interval,
                    feed.enabled,
                    feed.last_updated,
                    feed.notify_with_guid,
                    feed.url,
                ),
            )

    def delete_feed(self, feed: Feed):
        with self.conn as c:
            c.execute(
                """
                DELETE FROM feeds WHERE url = ?;
                """,
                (feed.url,),
            )

    def add_entry(self, entry: Entry, feed: Feed):
        with self.conn as c:
            c.execute(
                """
                INSERT INTO entries (
                    id, feed_url, title, link, published_timestamp
                ) VALUES (?,?,?,?,?);
                """,
                (
                    entry.id,
                    feed.url,
                    entry.title,
                    entry.link,
                    entry.published_timestamp,
                ),
            )

    def entry_exists(self, entry: Entry) -> bool:
        with self.conn as c:
            row = c.execute(
                """
                SELECT id FROM entries WHERE id = ?;
                """,
                (entry.id,),
            ).fetchone()
            return row is not None

    def get_recent_entries(self, feed: Feed, limit: int = 10) -> list[Entry]:
        return [
            Entry(**row)
            for row in self.conn.execute(
                """
                SELECT * FROM entries
                    WHERE feed_url = ?
                    ORDER BY published_timestamp DESC
                    LIMIT ?
                """,
                (feed.url, limit),
            )
        ]
