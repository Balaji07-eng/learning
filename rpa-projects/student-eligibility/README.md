# Student Eligibility Screening Automation

## Objective
Build a Power Automate Desktop flow that processes student records and returns an eligibility decision using age and marks.

**Status:** implementation guide; flow export and run evidence pending.

## Demonstration rules
These are invented practice rules, not admission policy:
- Student ID and name must be present.
- Age must be a whole number from 0 to 120.
- Marks must be numeric from 0 to 100.
- Eligible: age >= 18 AND marks >= 60.
- Invalid input: fail validation without attempting the eligibility decision.
- Otherwise: Not Eligible.

## Files
- input.csv: synthetic records.
- expected-results.csv: manually derived reference decisions.

## Build guide
1. Import input.csv into Excel and save as students.xlsx with headers in row 1.
2. Launch Excel and open the workbook. Read the used worksheet range into a data table, treating row 1 as column names.
3. Create an output worksheet with StudentID, Name, Status, and Reason headers.
4. Use For Each to iterate over data rows.
5. Read StudentID, Name, Age, and Marks into variables. Trim text and check required fields before numeric conversion.
6. Handle conversion failures as Invalid Input. Validate numeric ranges and the whole-number age requirement.
7. Use If/Else conditions to evaluate age and marks. Set Status and Reason using the rules above.
8. Write each result to the next available output row. Save and close Excel.

## Acceptance checks
- Compare all records against expected-results.csv.
- Confirm age 18 and marks 60 are eligible.
- Confirm blank age and marks above 100 are invalid.
- Confirm a failed conversion does not stop subsequent records.
- On rerun, clear the output rows below the header before processing so results are not duplicated.

## Evidence to add after implementation
Add exported/copied PAD flow actions, screenshots of the flow and output sheet, and a short description of your actual test results.
