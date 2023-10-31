# -*- coding: utf-8 -*-

"""
You can use one of the following hotkey to do anything using the selected item.

- :meth:`Enter <zelfred.item.Item.enter_handler>`
- :meth:`Ctrl + A <zelfred.item.Item.ctrl_a_handler>`
- :meth:`Ctrl + W <zelfred.item.Item.ctrl_w_handler>`
- :meth:`Ctrl + P <zelfred.item.Item.ctrl_p_handler>`

This module provides some common actions that you can use directly.
"""

import subprocess
from pathlib import Path

try:  # pragma: no cover
    from mac_notifications import client as mac_notification_client

    has_mac_notifications = True
except ImportError:  # pragma: no cover
    has_mac_notifications = False

try:  # pragma: no cover
    import pyperclip

    has_pyperclip = True
except ImportError:  # pragma: no cover
    has_pyperclip = False

from .vendor.os_platform import IS_WINDOWS


def open_url(url: str):  # pragma: no cover
    """
    Open a URL in the default browser.
    """
    if IS_WINDOWS:
        subprocess.run(["start", url], shell=True)
    else:
        subprocess.run(["open", url])


def open_file(path: Path):  # pragma: no cover
    """
    Open a file in the default application.
    """
    if IS_WINDOWS:
        subprocess.run([str(path)], shell=True)
    else:
        subprocess.run(["open", str(path)])


def copy_text(text: str):  # pragma: no cover
    """
    Copy text to clipboard.
    """
    if has_pyperclip is False:
        raise ImportError(
            "You need to do 'pip install pyperclip' first to copy text to clipboard."
        )
    pyperclip.copy(text)


def send_mac_notification(
    title: str,
    subtitle: str,
):  # pragma: no cover
    """
    Send a MAC notification.

    This feature is based on the
    `macos-notifications <https://github.com/Jorricks/macos-notifications>`_
    Python library.

    However, this is not working on MacOS > 11.0, because of the API this library
     is using is deprecated. See this discussion for more details
     https://github.com/Jorricks/macos-notifications/issues/8.
    """
    if has_mac_notifications is False:
        raise ImportError(
            "You need to do 'pip install mac_notifications' first to send notification."
        )

    mac_notification_client.create_notification(
        title=title,
        subtitle=subtitle,
    )
