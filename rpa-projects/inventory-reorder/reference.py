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
    key = row["SKU"].strip()
    if not key or not row["Item"].strip(): return key, "Missing required field", {}
    values = [number(row[name]) for name in ("Stock", "ReorderPoint", "TargetStock")]
    if any(v is None or v < 0 or v != v.to_integral_value() for v in values):
        return key, "Invalid stock values", {}
    stock, point, target = values
    if target <= point: return key, "Invalid target", {}
    return key, ("Reorder" if stock <= point else "Sufficient stock"), {"Quantity": str(int(target - stock)) if stock <= point else "0"}

def process(source, destination):
    seen = set()
    with open(source, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = "SKU,Item,Stock,ReorderPoint,TargetStock".split(",")
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
