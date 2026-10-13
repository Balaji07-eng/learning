# Expense Approval Screening

## Objective
Screens claims for human review. It does not approve claims, reimburse expenses, or send messages.

## Status
Runnable Python reference and Power Automate Desktop implementation guide. No exported PAD flow or PAD execution evidence is included. Sample rules and records are fictional.

## Rules
ClaimID and Employee required; Category must be Travel or Meals; positive finite Amount required; Receipt must be Yes or No. Missing receipt requires review. Claims above 2000 require manager review. Other valid claims are Eligible for approval. These are synthetic practice rules.
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
2. Read expense rows; validate text and numeric inputs; use nested If/Else for receipt and amount rules; write decision and amount to a results sheet; separate review cases for a human approver.
3. Track IDs of accepted records and reject repeated IDs within the batch.
4. Save results to a separate workbook and close Excel. Handle conversion and file errors explicitly.
5. Compare every decision with expected-results.csv before documenting the flow as completed.

## Further checks
Test blank required values, duplicate accepted IDs, nonnumeric values, an empty file with headers, and malformed CSV rows. Numeric NaN and infinity must fail validation. Rerunning the same input should reproduce the same report.

## Portfolio evidence to add
Export or copy PAD actions; add screenshots of the flow and results and actual test notes. Only claim PAD implementation on your resume after building and running it.
