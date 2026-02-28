import os
from typing import List, Dict, Optional
from agent.ai_analyzer import AIAnalyzer


class DependencyChecker:
    """
    Checks project dependencies for potential risks.
    Can optionally use AIAnalyzer for intelligent risk evaluation.
    """

    def __init__(self, ai_analyzer: Optional[AIAnalyzer] = None):
        self.ai_analyzer = ai_analyzer

    def check_dependencies(self, requirements_path: str) -> List[Dict]:
        """
        Analyze dependencies listed in requirements.txt.
        Returns structured list of dependency risks.
        """

        if not os.path.exists(requirements_path):
            return []

        dependencies = self._parse_requirements(requirements_path)
        results = []

        for dep in dependencies:
            result = self._analyze_dependency(dep)
            results.append(result)

        return results

    def _parse_requirements(self, file_path: str) -> List[str]:
        """
        Parse requirements.txt and extract dependency lines.
        """
        dependencies = []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                clean = line.strip()
                if clean and not clean.startswith("#"):
                    dependencies.append(clean)

        return dependencies

    def _analyze_dependency(self, dependency: str) -> Dict:
        """
        Basic dependency risk evaluation.
        If AIAnalyzer is available, use it for deeper inspection.
        """

        base_result = {
            "dependency": dependency,
            "risk_level": "UNKNOWN",
            "description": ""
        }

        # Basic heuristic (version pinning check)
        if "==" not in dependency:
            base_result["risk_level"] = "MEDIUM"
            base_result["description"] = "Dependency version not pinned. May introduce breaking or insecure updates."
        else:
            base_result["risk_level"] = "LOW"
            base_result["description"] = "Version pinned. No immediate structural risk detected."

        # Optional AI enhancement
        if self.ai_analyzer:
            try:
                ai_prompt = f"""
You are a cybersecurity expert.

Analyze this Python dependency for known security risks:

{dependency}

Return ONLY JSON:
{{
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "description": "string"
}}
"""
                response = self.ai_analyzer.model.generate_content(ai_prompt)
                import json
                ai_data = json.loads(response.text.strip())

                base_result.update(ai_data)

            except Exception:
                pass  # Fail silently, keep heuristic result

        return base_result