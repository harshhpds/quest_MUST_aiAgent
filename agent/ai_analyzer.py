import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


class AIAnalyzer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)

        # Use a stable model
        self.model = genai.GenerativeModel("gemini-2.5-pro")

    def analyze_code(self, code: str, file_path: str) -> dict:
        prompt = f"""
You are a cybersecurity expert.

Analyze the following code for security vulnerabilities.

Return ONLY valid JSON.
Do NOT include markdown.
Do NOT wrap in ```json.

Format:

{{
  "file": "{file_path}",
  "vulnerabilities": [
    {{
      "type": "string",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "line": int,
      "description": "string",
      "recommendation": "string"
    }}
  ]
}}

If no vulnerabilities, return:
{{
  "file": "{file_path}",
  "vulnerabilities": []
}}

Code:
{code}
"""

        try:
            response = self.model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty response from Gemini")

            cleaned = response.text.strip()

            # Remove accidental markdown blocks if model adds them
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]

            return json.loads(cleaned)

        except Exception as e:
            print(f"[AIAnalyzer Error] {e}")

            return {
                "file": file_path,
                "vulnerabilities": []
            }

    def generate_patch(self, code: str) -> str:
        prompt = f"""
You are a secure coding expert.

Rewrite the following code to fix all security vulnerabilities.

Return ONLY the fixed code.
Do NOT include explanations.
Do NOT wrap in markdown.

Code:
{code}
"""

        try:
            response = self.model.generate_content(prompt)

            if not response.text:
                return code

            cleaned = response.text.strip()

            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]

            return cleaned

        except Exception as e:
            print(f"[Patch Generation Error] {e}")
            return code