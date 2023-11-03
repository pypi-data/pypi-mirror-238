# wslconv

[![Version](https://img.shields.io/pypi/v/wslconv)](https://pypi.org/project/wslconv)
[![License](https://img.shields.io/pypi/l/wslconv)](https://github.com/lashahub/wslconv/blob/main/LICENSE)

A utility for converting file paths between WSL (Windows Subsystem for Linux) and Windows formats.

**wslconv** helps developers working with WSL, bridge the path differences between Windows and Linux, making the
experience smoother and error-free.

## Features

- Detect and convert paths automatically based on their format.
- Support for native Linux paths, native Windows paths, Linux paths on Windows, and Windows paths on Linux.
- Simple, intuitive API for developers.

## Installation

To install **wslconv**, use pip:

```
pip install wslconv
```

## Quickstart

Here's a quick example:

```python
from wslconv import WSLPathConverter

# Create an instance with the path and distro name
converter = WSLPathConverter("C:\\Users\\user\\Documents", "Ubuntu")

# Convert to Linux format
linux_path = converter.to_linux()
print(linux_path)  # Expected: /mnt/c/Users/user/Documents

# Convert to Windows format
windows_path = converter.to_windows()
print(windows_path)  # Expected: C:\Users\user\Documents
```

## API Reference

### `WSLPathConverter`

Main class for the path conversion.

#### Methods

- `__init__(self, path, distro)`: Initialize with a path and the name of the WSL distro.
- `filesystem_type(self)`: Return the filesystem type of the path (`Linux` or `Windows`).
- `os_type(self)`: Return the OS type based on the path format (`Linux` or `Windows`).
- `to_linux(self)`: Convert the path to its Linux representation.
- `to_windows(self)`: Convert the path to its Windows representation.

## Contributing

Feel free to open issues or PRs if you find any bugs or have suggestions for improvements!
