from typing import Dict
from agent.ai_analyzer import AIAnalyzer


class PatchGenerator:
    """
    Generates secure patches for vulnerable files
    using AIAnalyzer.
    """

    def __init__(self, ai_analyzer: AIAnalyzer):
        self.ai_analyzer = ai_analyzer

    def generate(self, file_path: str) -> Dict:
        """
        Generate patched version of a file.
        Returns structured result.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                original_code = f.read()
        except Exception:
            return {
                "file": file_path,
                "patched_code": None,
                "status": "error_reading_file"
            }

        try:
            patched_code = self.ai_analyzer.generate_patch(original_code)

            return {
                "file": file_path,
                "patched_code": patched_code,
                "status": "success"
            }

        except Exception:
            return {
                "file": file_path,
                "patched_code": None,
                "status": "patch_generation_failed"
            }