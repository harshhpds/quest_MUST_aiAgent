# CodeGuardian Agent

**CodeGuardian Agent** is an AI-powered cybersecurity tool designed to automatically scan your Python codebase for security vulnerabilities and dependency risks. Leveraging Google's latest Gemini generative AI, CodeGuardian identifies insecure code, hardcoded secrets, dependency issues, and will even suggest secure code patches.

---

## 🚩 Key Features

- **AI-Based Vulnerability Detection:** Utilizes Gemini (`gemini-2.5-pro`) to assess Python code files for security risks.
- **Patch Suggestion:** Automatically generates secure code improvements for detected issues.
- **Dependency Analysis:** Checks your Python dependencies (`requirements.txt`) for common risks such as unpinned versions.
- **Secret Detection:** Looks for hardcoded secrets and other risky patterns.
- **Comprehensive Reporting:** Generates detailed, timestamped JSON reports in the `reports/` directory.
- **Risk Scoring:** Assigns a risk score and level to your project based on findings.
- **Modular Architecture:** Easily extend or customize analysis modules as needed.
- **Prioritization:** Surfaces and prioritizes the most critical code risks.

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/codeguardian-agent.git
   cd codeguardian-agent
   ```

2. **Set Up Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   - Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Add it to a `.env` file at the project root:
     ```
     GEMINI_API_KEY=your-gemini-api-key-here
     ```

---

## 🚀 Usage

To scan all .py files in your repository and generate a report:
```bash
python main.py
```

After running, find your results as a JSON report under `reports/`.

---

## 🗂 Project Layout

```
codeguardian-agent/
│
├── agent/
│   ├── ai_analyzer.py            # Handles AI-driven code analysis and patching
│   ├── dependency_checker.py     # Scans and assesses your Python dependencies
│   ├── patch_generator.py        # (If present) Responsible for creating patches
│   ├── repo_scanner.py           # Recursively finds files to scan
│   └── vulnerability_detector.py # Additional vulnerability checks
│
├── metrics/
│   └── risk_score.py             # Aggregates vulnerability and risk data
│
├── reports/                      # Output folder for scan results
│
├── main.py                       # Entry point for running the CodeGuardian agent
├── requirements.txt              # Python dependencies
├── .env                          # API key for Gemini (not committed)
└── README.md
```

---

## 🎯 What Gets Scanned?
- All Python files in your project.
- Your `requirements.txt` for dependency issues (e.g., unpinned versions).
- Any other files as configured in the source code.

---

## 📋 Example Scan Report

Sample JSON output (`reports/report_YYYYMMDD_HHMMSS.json`):
```json
{
    "scan_target": ".",
    "scan_timestamp": "...",
    "vulnerabilities": [
        {
            "file": "./main.py",
            "vulnerabilities": []
        },
        ...
    ],
    "dependency_analysis": [
        {
            "dependency": "google-generativeai",
            "risk_level": "MEDIUM",
            "description": "Dependency version not pinned. May introduce breaking or insecure updates."
        },
        ...
    ],
    "risk_summary": {
        "score": 0.0,
        "risk_level": "LOW",
        "total_vulnerabilities": 0
    },
    "patches": []
}
```

---

## 📝 Custom Rules/Focus Areas

As described in `.cursorrules`, CodeGuardian focuses on:

- **SQL injection**
- **Hardcoded secrets** (e.g., credentials, API keys)
- **`eval()` usage**
- **Dependency vulnerabilities** (like unpinned package versions)

---

## ⚠️ Security & Usage Notes

- **Never commit your `.env` or API keys to version control.**
- Scan results should be reviewed by a human—AI suggestions can have limitations.
- Patch generation is intended to assist; always review before applying.
- The tool currently supports Python and expects Python-style projects.

---

## 💡 Advanced Usage & Extending

- To add new vulnerability checks or customize behavior, extend files in `agent/`.
- To change scan targets, modify the logic in `repo_scanner.py`.
- All analyzer prompts are in `ai_analyzer.py` and can be refined for new threats.

---

## 🤝 Contributing

Contributions are welcome! Open an issue or pull request for improvements, bug fixes, or new features.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for complete terms.

---

## 🙏 Credits

- [Google Gemini (generativeai)](https://ai.google.com/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 🏁 Getting Help

If you have questions, open an issue or reach out via GitHub Discussions.

---

**Stay secure — automate your code reviews with CodeGuardian Agent!**
