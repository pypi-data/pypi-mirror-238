<!--
Author: Nabil El Ouaamari (nabil.elouaamari.dev@gmail.com)
README.md (c) 2023
Desc: README file for Colorful Debug
-->

# Colorful Debug

Author: Nabil El Ouaamari (nabil.elouaamari.dev@gmail.com)

## Description

Colorful Debug is a Python module that provides colorful and customizable debug print messages with timestamps. It's designed to make debugging your applications more user-friendly and visually appealing.

## Installation

You can install Colorful Debug using pip:

```bash
pip install colorful-debug
```

## Usage
```py
from colorful_debug import ColorfulDebug

# As default, timestamp and bold font are enabled
debug = ColorfulDebug(show_timestamp=True, all_bold=False)

# Print debug messages with different message types
debug.print(message, msg_type="normal", ov_bold=None)           # default behavior, 'ov_bold' overrides all_bold
debug.print("This is a normal message")                         # color is 'white' by default
debug.print("This is a warning message", msg_type="warning")    # color is 'yellow' by default
debug.print("This is an info message", msg_type="info")         # color is 'cyan' by default
debug.print("This is an error message", msg_type="error")       # color is 'red' by default
```

## Customization
    
```py
# Customize color and prefix for different message types
debug.set_color("warning", "yellow")
debug.set_prefix("info", "[Info]")

# Disable timestamp
debug.set_show_timestamp(False)

# Create a new message type
debug.new_message_type("success", prefix="[Success]", suffix="", color="green", bold=False)

# Use the new message type
debug.print("This is a success message", msg_type="success")

# Update the new message type
debug.set_color("success", "blue")
debug.set_prefix("success", "[OK]")
debug.set_suffix("success", " (OK)")
debug.set_bold("success", True)
```

## Configuration

You can configure Colorful Debug to fit your needs. Customize colors, prefixes, timestamps, and more.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact / Support

If you have any questions, suggestions, or concerns, feel free to contact me at nabil.elouaamari.dev@gmail.com.

## Acknowledgements

* [Termcolor](https://pypi.org/project/termcolor/)