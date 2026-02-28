import os
import sys
import json
import datetime

from agent.repo_scanner import RepoScanner
from agent.ai_analyzer import AIAnalyzer
from agent.vulnerability_detector import VulnerabilityDetector
from agent.patch_generator import PatchGenerator
from agent.dependency_checker import DependencyChecker
from metrics.risk_score import calculate_risk_score


def ensure_reports_directory():
    if not os.path.exists("reports"):
        os.makedirs("reports")


def save_report(report_data: dict) -> str:
    ensure_reports_directory()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    return report_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <repository_path>")
        sys.exit(1)

    target_path = sys.argv[1]

    if not os.path.exists(target_path):
        print("Provided path does not exist.")
        sys.exit(1)

    print("\n[+] Initializing AI Analyzer...")
    ai_analyzer = AIAnalyzer()

    print("[+] Scanning repository...")
    scanner = RepoScanner()
    files = scanner.scan(target_path)

    print(f"[+] Found {len(files)} source files.")

    print("[+] Detecting vulnerabilities...")
    detector = VulnerabilityDetector(ai_analyzer)
    vulnerability_results = detector.analyze_repository(target_path, files)

    print("[+] Checking dependencies...")
    dependency_checker = DependencyChecker(ai_analyzer)
    dependency_results = dependency_checker.check_dependencies(
        os.path.join(target_path, "requirements.txt")
    )

    print("[+] Calculating risk score...")
    risk_summary = calculate_risk_score(vulnerability_results)

    print("[+] Generating patches for vulnerable files...")
    patch_generator = PatchGenerator(ai_analyzer)
    patches = []

    for file_result in vulnerability_results:
        if file_result.get("vulnerabilities"):
            patch_result = patch_generator.generate(file_result["file"])
            patches.append(patch_result)

    report = {
        "scan_target": target_path,
        "scan_timestamp": datetime.datetime.now().isoformat(),
        "vulnerabilities": vulnerability_results,
        "dependency_analysis": dependency_results,
        "risk_summary": risk_summary,
        "patches": patches
    }

    report_path = save_report(report)

    print("\n========== SCAN SUMMARY ==========")
    print(f"Total Vulnerabilities: {risk_summary['total_vulnerabilities']}")
    print(f"Risk Score: {risk_summary['score']}/100")
    print(f"Risk Level: {risk_summary['risk_level']}")
    print(f"Report saved to: {report_path}")
    print("===================================\n")


if __name__ == "__main__":
    main()