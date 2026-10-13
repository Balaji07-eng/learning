# Inventory Reorder Report

## Objective
Produces a replenishment recommendation only; no orders are placed.

## Status
Runnable Python reference and Power Automate Desktop implementation guide. No exported PAD flow or PAD execution evidence is included. Sample rules and records are fictional.

## Rules
SKU and Item required; Stock, ReorderPoint and TargetStock must be nonnegative whole numbers; TargetStock must exceed ReorderPoint. Stock <= ReorderPoint triggers Reorder with Quantity = TargetStock - Stock.
Duplicates are checked against earlier accepted records in this input batch. Invalid records do not reserve their ID. The reference does not persist processed IDs between runs.

## Run the Python reference
Requires Python 3.9+; no external packages.
```sh
python reference.py
python reference.py input.csv results.csv
```
Run from this folder. The default output is results.csv and is replaced on each run. The input remains unchanged. Compare results with expected-results.csv. Value holds an amount; Quantity holds a reorder count.

## Build in Power Automate Desktop
1. Import input.csv into Excel and save as .xlsx.
2. Read inventory sheet; validate whole-number fields; use If/Else to compare Stock against ReorderPoint; calculate replenishment quantity using variables; write a report; filter Reorder rows into a purchase-review sheet.
3. Track IDs of accepted records and reject repeated IDs within the batch.
4. Save results to a separate workbook and close Excel. Handle conversion and file errors explicitly.
5. Compare every decision with expected-results.csv before documenting the flow as completed.

## Further checks
Test blank required values, duplicate accepted IDs, nonnumeric values, an empty file with headers, and malformed CSV rows. Numeric NaN and infinity must fail validation. Rerunning the same input should reproduce the same report.

## Portfolio evidence to add
Export or copy PAD actions; add screenshots of the flow and results and actual test notes. Only claim PAD implementation on your resume after building and running it.
