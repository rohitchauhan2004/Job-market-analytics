# src/etl/utils.py

import re

def normalize_title(t: str) -> str:
    t = t.lower()
    # keep only a-z, 0-9, space, +, #, -, /
    t = re.sub(r"[^a-z0-9 +#\-/]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def split_location(loc):
    if not loc: return None, None, None
    parts = [p.strip() for p in re.split(r",|\\|", loc) if p.strip()]
    city = parts[0] if len(parts) > 0 else None
    state = parts[1] if len(parts) > 1 else None
    country = parts[2] if len(parts) > 2 else None
    return city, state, country

def parse_salary(text):
    text = text or ""
    # ₹8-12 LPA
    m = re.search(r"(₹|\\$)?\\s*([\\d,.]+)\\s*[-to]{1,3}\\s*([\\d,.]+)\\s*(lpa|lac|lakh|per annum|pa|year)", text, re.I)
    if m:
        cur = m.group(1) or "₹"
        lo = float(m.group(2).replace(",", ""))
        hi = float(m.group(3).replace(",", ""))
        if re.search(r"lpa|lac|lakh", m.group(4), re.I):
            lo *= 100000; hi *= 100000
            cur = "₹"
        return lo, hi, cur, "year"
    # $80k/year
    m = re.search(r"(₹|\\$)?\\s*([\\d,.]+)\\s*(k|m)?\\s*/?\\s*(year|annum|month)", text, re.I)
    if m:
        cur = m.group(1) or None
        val = float(m.group(2).replace(",", ""))
        unit = (m.group(3) or "").lower()
        per = m.group(4).lower()
        if unit == "k": val *= 1000
        if unit == "m": val *= 1000000
        return val, None, cur, "year" if "year" in per or "annum" in per else "month"
    return None, None, None, None
