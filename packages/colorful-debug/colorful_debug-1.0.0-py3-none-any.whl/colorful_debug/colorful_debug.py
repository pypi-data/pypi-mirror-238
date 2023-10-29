"""
Author: Nabil El Ouaamari (nabil.elouaamari.dev@gmail.com)
colorful_debug.py (c) 2023
Desc: A simple debug class that allows you to print colorful messages to the console.
"""
# colorful_debug.py

__version__ = "1.0.0"
import datetime
from termcolor import colored
import os

class ColorfulDebug:
    """
    A simple debug class that allows you to print colorful messages to the console.
    """

    def __init__(self, show_timestamp=True, all_bold=False):
        """
        Initialize the ColorfulDebug instance.
        :param show_timestamp: Whether to show timestamps.
        :param all_bold: Whether to make all messages bold.
        """
        
        self.show_timestamp = show_timestamp
        self.prefix_map = {
            "normal": {"prefix": "", "suffix": ""},
            "warning": {"prefix": "[Warning]", "suffix": ""},
            "info": {"prefix": "[Info]", "suffix": ""},
            "error": {"prefix": "[Error]", "suffix": ""},
        }
        self.color_map = {
            "normal": {"color": "white", "bold": all_bold},
            "warning": {"color": "yellow", "bold": all_bold},
            "info": {"color": "cyan", "bold": all_bold},
            "error": {"color": "red", "bold": all_bold},
        }

    def set_color(self, msg_type, color, bold=False):
        """
        Set the color for a message type.
        :param msg_type: The message type.
        :param color: The color.
        :param bold: Whether to make the message bold.
        """

        if msg_type in self.color_map:
            self.color_map[msg_type]["color"] = color
            self.color_map[msg_type]["bold"] = bold
        else:
            print(f"Message type '{msg_type}' does not exist in the color map.")

    def set_prefix(self, msg_type, prefix, suffix=""):
        """
        Set the prefix for a message type.
        :param msg_type: The message type.
        :param prefix: The prefix.
        :param suffix: The suffix.
        """

        if msg_type in self.prefix_map:
            self.prefix_map[msg_type]["prefix"] = prefix
            self.prefix_map[msg_type]["suffix"] = suffix
        else:
            print(f"Message type '{msg_type}' does not exist in the prefix map.")

    def set_show_timestamp(self, show_timestamp):
        """
        Set whether to show timestamps.
        :param show_timestamp: Whether to show timestamps.
        """

        self.show_timestamp = show_timestamp

    def new_message_type(self, msg_type, prefix="", suffix="", color="white", bold=False):
        """
        Create a new message type.
        :param msg_type: The message type.
        :param prefix: The prefix.
        :param suffix: The suffix.
        :param color: The color.
        :param bold: Whether to make the message bold.
        """

        self.prefix_map[msg_type] = {"prefix": prefix, "suffix": suffix}
        self.color_map[msg_type] = {"color": color, "bold": bold}

    def print(self, message, msg_type="normal", ov_bold=None):
        """
        Print a message.
        :param message: The message.
        :param msg_type: The message type.
        :param ov_bold: Override the bold setting for this message.
        """
        
        timestamp = ""
        if self.show_timestamp:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            timestamp = f"[{current_time}] "

        prefix = self.prefix_map.get(msg_type, {}).get("prefix", "")
        suffix = self.prefix_map.get(msg_type, {}).get("suffix", "")
        color = self.color_map.get(msg_type, {}).get("color", "white")
        if ov_bold is not None:
            bold = ov_bold
        else:
            bold = self.color_map.get(msg_type, {}).get("bold", False)
        
        if prefix:
            prefix = f"{prefix} "
        if suffix:
            suffix = f" {suffix}"

        tmsp = colored(timestamp, color, attrs=['bold'])
        colored_message = colored(f"{prefix}{message}{suffix}", color, attrs=[] if not bold else ['bold'])

        if self.show_timestamp:
            print(f"{tmsp}{colored_message}")
        else:
            print(colored_message)

if __name__ == "__main__":
    # Example usage:
    debug = ColorfulDebug(show_timestamp=True, all_bold=False)

    debug.print("This is a normal message")
    debug.print("This is a warning message", msg_type="warning", ov_bold=True)
    debug.print("This is an info message", msg_type="info")
    debug.print("This is an error message", msg_type="error")

    # Modify color settings, prefixes, and suffixes
    # debug.set_color("normal", "green", bold=False)
    # debug.set_prefix("info", "[NewInfo]", suffix="[End]")
    # debug.set_prefix("warning", "[Custom Warning]", suffix="(custom)")

    # debug.print("Custom color, bold and suffix for 'normal'", msg_type="normal")
    # debug.print("Custom color and suffix for 'info'", msg_type="info")
    # debug.print("Custom prefix and suffix for 'warning'", msg_type="warning")
