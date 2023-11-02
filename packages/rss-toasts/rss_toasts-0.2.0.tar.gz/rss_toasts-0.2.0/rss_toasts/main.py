import importlib.resources
import io
import time
from functools import partial
from threading import Event

import pystray  # type: ignore
from PIL import Image
from windows_toasts import Toast, WindowsToaster

from rss_toasts.db import Database
from rss_toasts.feed import Entry, Feed
from rss_toasts.gui import start_gui


def _print(msg: str) -> None:
    print(f"[{time.ctime()}] {msg}")


def toast(toaster: WindowsToaster, feed: Feed, entry: Entry):
    newToast = Toast()
    newToast.text_fields = [
        feed.title + "\n",
        entry.title,
        "\nClick to open",
    ]
    if feed.notify_with_guid:
        newToast.launch_action = entry.id
    else:
        newToast.launch_action = entry.link
    toaster.show_toast(newToast)


def icon_setup(icon: pystray.Icon, exit_event: Event):
    icon.visible = True

    toaster = WindowsToaster("rss-toasts")

    try:
        while not exit_event.is_set():
            with Database() as db:
                for feed in db.get_feeds():
                    if time.time() < feed.last_updated + feed.update_interval:
                        continue
                    _print(f"Updating feed: {feed.url}")
                    try:
                        entries = feed.get_entries()
                    except Exception as e:
                        _print(f"Error updating feed: {e}")
                        continue
                    else:
                        for entry in entries:
                            if db.entry_exists(entry):
                                continue
                            db.add_entry(entry, feed)
                            _print(f"New entry: {entry.title} {entry.link}")
                            toast(toaster, feed, entry)
                        feed.last_updated = int(time.time())
                        db.update_feed(feed)
            exit_event.wait(60)
    except Exception as e:
        _print(f"Unhandled exception: {e}")
    except KeyboardInterrupt:
        pass

    _print("Exiting...")
    icon.stop()


def systray():
    icon_image = Image.open(
        io.BytesIO(importlib.resources.read_binary("rss_toasts", "icon.ico"))
    )

    exit_event = Event()

    icon = pystray.Icon(
        "rss-toasts",
        icon=icon_image,
        title="rss-toasts",
        menu=pystray.Menu(
            pystray.MenuItem("Feeds", start_gui),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", exit_event.set),
        ),
    )

    setup = partial(icon_setup, exit_event=exit_event)
    icon.run(setup)  # type: ignore


def main():
    systray()


if __name__ == "__main__":
    main()
