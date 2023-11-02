import gc
import time
import webbrowser
from datetime import datetime
from tkinter import BooleanVar, IntVar, StringVar, Tk, messagebox, simpledialog, ttk
from typing import Any

import requests

from rss_toasts.db import Database
from rss_toasts.feed import Feed

DEFAULT_UPDATE_INTERVAL = 1800
UPDATE_INTERVAL_MIN = 300


class FeedsGui(Tk):
    def __init__(self, db: Database):
        self.db = db
        self.feeds: list[Feed] = []

        super().__init__()
        self.title("rss-toasts - Feeds")
        frm = ttk.Frame(self, padding=10)
        frm.grid(column=0, row=0, sticky="nsew")

        # Feed selection combobox
        cb_frm = ttk.Frame(frm)
        cb_frm.grid(row=0, column=0, sticky="we")
        ttk.Label(cb_frm, text="Feed: ").grid(row=0, column=0, sticky="we")

        self.selected_feed = StringVar()
        self.combobox = ttk.Combobox(
            cb_frm,
            textvariable=self.selected_feed,
        )
        self.combobox.state(["readonly"])  # type: ignore
        self.combobox.grid(row=0, column=1, sticky="we")
        self.combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # Feed edit form
        form_frm = ttk.LabelFrame(frm, text="Edit", padding=10)
        form_frm.grid(row=1, column=0, sticky="wen", pady=10)

        def validate_number_func(value: str) -> bool:
            return value.isdigit() or value == ""

        validate_number = (self.register(validate_number_func), "%P")

        self.form_url = StringVar()
        self.form_update_interval = IntVar()
        self.form_enabled = BooleanVar()
        self.form_notify_with_guid = BooleanVar()
        ttk.Label(form_frm, text="URL: ").grid(row=0, column=0, sticky="we")
        ttk.Label(form_frm, text="Update Interval: ").grid(row=1, column=0, sticky="we")
        ttk.Entry(form_frm, textvariable=self.form_url).grid(
            row=0, column=1, sticky="we"
        )
        ttk.Entry(
            form_frm,
            textvariable=self.form_update_interval,
            validate="key",
            validatecommand=validate_number,
        ).grid(row=1, column=1, sticky="we")
        ttk.Checkbutton(form_frm, text="Enabled", variable=self.form_enabled).grid(
            row=2, column=1, sticky="we"
        )
        ttk.Checkbutton(
            form_frm,
            text="Notify with GUID instead of Link"
            " (useful for some feeds that direct link to a file)",
            variable=self.form_notify_with_guid,
        ).grid(row=3, column=1, sticky="we")
        self.form_btn_save = ttk.Button(form_frm, text="Save", command=self.save_feed)
        self.form_btn_save.grid(row=4, column=0, sticky="w")
        self.form_btn_del = ttk.Button(
            form_frm, text="Delete", command=self.delete_feed
        )
        self.form_btn_del.grid(row=4, column=1, sticky="e")

        # Recent feed entries
        ttk.Label(form_frm, text="Recent entries (double-click to open):").grid(
            row=5, column=0, columnspan=2, sticky="we", pady=(10, 0)
        )
        tree = ttk.Treeview(form_frm, columns=("published", "title"), show="headings")
        tree.grid(row=6, column=0, columnspan=2, sticky="we")
        tree.column("published", width=125, stretch=False)
        tree.heading("published", text="Published")
        tree.heading("title", text="Title")
        tree.bind("<Double-Button-1>", self.feed_entry_double_clicked)
        self.feed_entries_treeview = tree

        # Add and Close Buttons
        ctrl_frm = ttk.Frame(frm)
        ctrl_frm.grid(row=2, column=0, sticky="wes")
        ttk.Button(ctrl_frm, text="Add Feed", command=self.add_feed_callback).grid(
            row=0, column=0, sticky="ws"
        )
        ttk.Button(ctrl_frm, text="Close", command=self.destroy).grid(
            row=0, column=1, sticky="es"
        )

        self.update_feeds()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        frm.columnconfigure(0, weight=1)
        frm.rowconfigure(2, weight=1)
        cb_frm.columnconfigure(0, weight=0)
        cb_frm.columnconfigure(1, weight=1)
        form_frm.columnconfigure(1, weight=1)
        ctrl_frm.columnconfigure(1, weight=1)

        self.center_window(640, 500)
        self.focus_force()

    def destroy(self) -> None:
        super().destroy()
        # call garbage collection to prevent
        # Tcl_AsyncDelete: async handler deleted by the wrong thread
        gc.collect()

    def center_window(self, width: int, height: int):
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def get_feed_by_url(self, url: str | None = None) -> Feed | None:
        if url is None:
            url = self.selected_feed.get()
        return next((feed for feed in self.feeds if feed.url == url), None)

    def combobox_selected(self, event: Any):
        feed = self.get_feed_by_url()
        self.combobox.selection_clear()
        if feed:
            self.populate_form(feed)
        else:
            self.update_feeds()

    def feed_entry_double_clicked(self, event: Any):
        feed = self.get_feed_by_url()
        if not feed:
            self.update_feeds()
            return

        focused_id = self.feed_entries_treeview.focus()
        entry = next(
            (entry for entry in self.feed_entries if entry.id == focused_id), None
        )
        if entry:
            if feed.notify_with_guid:
                url = entry.id
            else:
                url = entry.link
            webbrowser.open(url)

    def populate_form(self, feed: Feed):
        self.form_url.set(feed.url)
        self.form_update_interval.set(feed.update_interval)
        self.form_enabled.set(feed.enabled)
        self.form_notify_with_guid.set(feed.notify_with_guid)
        self.feed_entries_treeview.delete(*self.feed_entries_treeview.get_children())
        self.feed_entries = self.db.get_recent_entries(feed)
        for entry in self.feed_entries:
            self.feed_entries_treeview.insert(
                "",
                "end",
                entry.id,
                values=(datetime.fromtimestamp(entry.published_timestamp), entry.title),
            )

    def update_feeds(self, select: str | None = None):
        self.feeds = self.db.get_feeds()
        if self.feeds:
            self.combobox["values"] = [feed.url for feed in self.feeds]
            if select and (feed := self.get_feed_by_url(select)):
                self.selected_feed.set(select)
                self.populate_form(feed)
            else:
                self.selected_feed.set(self.feeds[0].url)
                self.populate_form(self.feeds[0])
            self.form_btn_save.state(["!disabled"])  # type: ignore
            self.form_btn_del.state(["!disabled"])  # type: ignore
        else:
            self.combobox["values"] = []
            self.form_url.set("")
            self.form_update_interval.set(DEFAULT_UPDATE_INTERVAL)
            self.form_enabled.set(True)
            self.form_btn_save.state(["disabled"])  # type: ignore
            self.form_btn_del.state(["disabled"])  # type: ignore

    def save_feed(self):
        feed = self.get_feed_by_url()
        if not feed:
            self.update_feeds()
            return
        feed.enabled = self.form_enabled.get()
        feed.url = self.form_url.get()
        feed.update_interval = self.form_update_interval.get()
        feed.enabled = self.form_enabled.get()
        feed.notify_with_guid = self.form_notify_with_guid.get()
        self.db.update_feed(feed)
        messagebox.showinfo(  # type: ignore
            title="Updated feed",
            message="Feed updated successfully",
            parent=self,
        )

    def delete_feed(self):
        feed = self.get_feed_by_url()
        if not feed:
            self.update_feeds()
            return
        if messagebox.askyesno(  # type: ignore
            title="Delete Feed",
            message=f"Are you sure you want to delete this feed?\n{feed.url}",
            parent=self,
        ):
            self.db.delete_feed(feed)
            messagebox.showinfo(  # type: ignore
                title="Deleted feed", message="Feed deleted successfully", parent=self
            )
            self.update_feeds()

    def validate_url(self, url: str) -> bool:
        if url:
            try:
                with requests.head(url, timeout=15.0) as r:
                    if r.ok:
                        return True
            except requests.RequestException:
                pass
        return False

    def add_feed_callback(self):
        feed = self.add_feed()
        if not feed:
            messagebox.showwarning(  # type: ignore
                title="Add Feed", message="Feed was not added", parent=self
            )
        else:
            messagebox.showinfo(  # type: ignore
                title="Add Feed", message="Feed added successfully", parent=self
            )
            self.update_feeds(select=feed.url)

    def add_feed(self) -> Feed | None:
        title = "Add Feed"

        feed = Feed()
        url = simpledialog.askstring(
            title=title,
            prompt="Enter the URL of the feed you wish to add",
            parent=self,
        )
        if not url or not self.validate_url(url):
            messagebox.showwarning(  # type: ignore
                title=title, message="Invalid URL", parent=self
            )
            return None
        feed.url = url

        update_interval = simpledialog.askinteger(
            title=title,
            prompt="Enter the update interval in seconds",
            initialvalue=DEFAULT_UPDATE_INTERVAL,
            minvalue=UPDATE_INTERVAL_MIN,
            parent=self,
        )
        if not update_interval:
            return None
        feed.update_interval = update_interval

        feed.enabled = messagebox.askyesno(  # type: ignore
            title=title,
            message="Do you wish to enable the feed?",
            parent=self,
        )

        feed.last_updated = int(time.time())
        if not self.db.add_feed(feed):
            return None
        if entries := feed.get_entries():
            for entry in entries:
                self.db.add_entry(entry, feed)
        return feed


def start_gui():
    with Database() as db:
        gui = FeedsGui(db)
        gui.mainloop()


if __name__ == "__main__":
    start_gui()
