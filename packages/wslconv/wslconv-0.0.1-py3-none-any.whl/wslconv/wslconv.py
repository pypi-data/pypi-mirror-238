class WSLPathConverter:
    def __init__(self, path, distro):
        self._win_on_linux_prefix = "/mnt/"
        self._linux_on_win_prefix = f"\\\\wsl.localhost\\{distro}\\"
        self._distro = distro
        self._path_format = None
        self._path_segments = None
        self._parse_path(path)

    def _parse_path(self, path):
        """Parse and identify the format of the given path."""
        if not path:
            raise ValueError("Path cannot be None or empty.")

        prefix = self._linux_on_win_prefix + 'mnt\\'
        if path.startswith(prefix):
            path = path[len(prefix)].upper() + ':' + path[len(prefix) + 1:]

        if path.startswith(self._win_on_linux_prefix):
            self._path_format = "WindowsOnLinux"
            self._path_segments = path[len(self._win_on_linux_prefix):].split("/")
        elif "\\" in path:
            if path.startswith(self._linux_on_win_prefix):
                self._path_format = "LinuxOnWindows"
                self._path_segments = path.split(self._linux_on_win_prefix)[1].split("\\")
            else:
                self._path_format = "WindowsNative"
                parts = path.split("\\")
                parts[0] = parts[0].lower().replace(':', '')
                self._path_segments = parts
        else:
            self._path_format = "LinuxNative"
            self._path_segments = path.strip("/").split("/")

    def filesystem_type(self):
        """Return the filesystem type of the path."""
        if self._path_format in ["LinuxNative", "LinuxOnWindows"]:
            return "Linux"
        elif self._path_format in ["WindowsNative", "WindowsOnLinux"]:
            return "Windows"

    def os_type(self):
        """Return the OS type based on the path format."""
        if self._path_format in ["WindowsOnLinux", "LinuxNative"]:
            return "Linux"
        elif self._path_format in ["LinuxOnWindows", "WindowsNative"]:
            return "Windows"

    def to_linux(self):
        """Convert the path to its Linux representation."""
        if self.filesystem_type() == "Linux":
            return "/" + "/".join(self._path_segments)
        else:
            return self._win_on_linux_prefix + "/".join(self._path_segments)

    def to_windows(self):
        """Convert the path to its Windows representation."""
        if self.filesystem_type() == "Windows":
            drive = self._path_segments[0].upper() + ":\\"
            return drive + "\\".join(self._path_segments[1:])
        else:
            return self._linux_on_win_prefix + "\\".join(self._path_segments)
