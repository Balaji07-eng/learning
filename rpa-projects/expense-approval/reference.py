"""Synthetic learning reference; this is Python, not a PAD flow export."""
import csv
import sys
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import date

def number(value):
    try:
        value = Decimal(value.strip())
        return value if value.is_finite() else None
    except InvalidOperation:
        return None

def evaluate(row):
    key = row["ClaimID"].strip()
    if not key or not row["Employee"].strip(): return key, "Missing required field", {}
    if row["Category"] not in ("Travel", "Meals"): return key, "Invalid category", {}
    amount = number(row["Amount"])
    if amount is None or amount <= 0: return key, "Invalid amount", {}
    if row["Receipt"] not in ("Yes", "No"): return key, "Invalid receipt flag", {}
    status = "Receipt review" if row["Receipt"] == "No" else ("Manager review" if amount > 2000 else "Eligible for approval")
    return key, status, {"Value": str(amount)}

def process(source, destination):
    seen = set()
    with open(source, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = "ClaimID,Employee,Category,Amount,Receipt".split(",")
        if reader.fieldnames != required:
            raise ValueError("Unexpected CSV headers: expected " + ",".join(required))
        results = []
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("Malformed CSV row")
            key, status, details = evaluate(row)
            accepted = status in ("Valid", "Eligible for approval", "Receipt review", "Manager review", "Reorder", "Sufficient stock")
            if accepted and key in seen:
                status, details = "Duplicate ID", {}
            elif accepted:
                seen.add(key)
            results.append({"ID": key, "Status": status, "Value": details.get("Value", ""), "Quantity": details.get("Quantity", "")})
    with open(destination, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["ID", "Status", "Value", "Quantity"])
        writer.writeheader()
        writer.writerows(results)
    return results

if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / "input.csv"
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else folder / "results.csv"
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output must be different files")
    results = process(source, destination)
    print(f"Wrote {len(results)} decisions to {destination}")
