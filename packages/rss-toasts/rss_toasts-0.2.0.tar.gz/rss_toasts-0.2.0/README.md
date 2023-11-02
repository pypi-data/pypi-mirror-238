# rss-toasts

## RSS toast notifications for Windows

A python script that sends toast notifications for new entries in RSS feeds.

Created due to a lack of simple RSS feed notifiers for Windows.
Most apps have not been updated in over 10 years and break for various reasons
like outdated SSL libraries.

## Usage

Requires `Python 3.11+` with `tkinter`.

Install using [pipx](https://pypa.github.io/pipx/):

```console
pipx install rss-toasts
```

Run it with console output:

```console
rss-toasts
```

Run it in the background without console window:

```console
rss-toasts-bg
```

The script will start minimized to the system tray.
Right-click the tray icon to manage feeds or close the script.
