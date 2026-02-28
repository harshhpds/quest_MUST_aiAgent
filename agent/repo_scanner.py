import os
from typing import List


class RepoScanner:
    """
    Scans a repository and returns a list of source code files
    while ignoring unnecessary directories.
    """

    def __init__(self):
        self.ignored_dirs = {
            "venv",
            "env",
            "__pycache__",
            "node_modules",
            ".git",
            "reports",
            ".idea",
            ".vscode"
        }

        self.allowed_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx"
        }

    def scan(self, root_path: str) -> List[str]:
        """
        Recursively scan repository and collect valid source files.
        """
        collected_files = []

        for root, dirs, files in os.walk(root_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file in files:
                if self._is_valid_file(file):
                    full_path = os.path.join(root, file)
                    collected_files.append(full_path)

        return collected_files

    def _is_valid_file(self, filename: str) -> bool:
        """
        Check if file extension is allowed.
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.allowed_extensions