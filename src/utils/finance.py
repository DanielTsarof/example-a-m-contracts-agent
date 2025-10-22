from typing import List


def hhi(shares: List[float]) -> int:
    """Herfindahl–Hirschman Index in points: 10000 * sum(s_i^2), s_i ∈ [0..1]."""
    return int(round(10000 * sum(s * s for s in shares)))


def wacc(beta: float, rf: float, erp: float, kd: float, tax: float, debt_ratio: float) -> float:
    """Simple WACC: (1-D)*Ke + D*Kd*(1-T)."""
    ke = rf + beta * erp
    d = max(0.0, min(1.0, debt_ratio))
    return (1 - d) * ke + d * kd * (1 - tax)


def score_map(value: str, mapping: dict, default: float = 0.5) -> float:
    """Safe display of string status in [0..1]."""
    return float(mapping.get(value, default))
