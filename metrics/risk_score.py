from typing import List, Dict


SEVERITY_WEIGHTS = {
    "CRITICAL": 10,
    "HIGH": 7,
    "MEDIUM": 4,
    "LOW": 1
}


def calculate_risk_score(vulnerability_results: List[Dict]) -> Dict:
    """
    Calculate overall repository risk score based on vulnerabilities.

    Returns:
    {
        "score": float (0-100),
        "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
        "total_vulnerabilities": int
    }
    """

    total_weight = 0
    total_vulnerabilities = 0

    for file_result in vulnerability_results:
        vulnerabilities = file_result.get("vulnerabilities", [])
        total_vulnerabilities += len(vulnerabilities)

        for vuln in vulnerabilities:
            severity = vuln.get("severity", "LOW").upper()
            weight = SEVERITY_WEIGHTS.get(severity, 1)
            total_weight += weight

    if total_vulnerabilities == 0:
        return {
            "score": 0.0,
            "risk_level": "LOW",
            "total_vulnerabilities": 0
        }

    # Normalize score to 0–100 scale
    max_possible_weight = total_vulnerabilities * SEVERITY_WEIGHTS["CRITICAL"]
    score = (total_weight / max_possible_weight) * 100

    risk_level = _determine_risk_level(score)

    return {
        "score": round(score, 2),
        "risk_level": risk_level,
        "total_vulnerabilities": total_vulnerabilities
    }


def _determine_risk_level(score: float) -> str:
    """
    Convert numeric score into risk level.
    """

    if score >= 75:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    else:
        return "LOW"