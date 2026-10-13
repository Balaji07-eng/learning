# Excel Data Entry and Worksheet Processing

## Objective
Build a Power Automate Desktop flow that validates incoming records and appends valid entries to an Excel master worksheet.

**Status:** implementation guide; flow export and run evidence pending.

## Demonstration rules
- RecordID and Name are required after trimming whitespace.
- Department must be Sales, Support, or Operations.
- Amount must be numeric and greater than zero.
- RecordID must be unique across the existing master and earlier accepted rows in the current batch.
- Invalid and duplicate entries go to an exceptions worksheet with a reason.
- Add an ID to the accepted-ID list only after validation and a successful write.

## Files
- master-seed.csv: initial master data.
- incoming.csv: synthetic new records.
- expected-master.csv: reference master after one successful run.
- expected-exceptions.csv: rejected rows and reasons.

## Build guide
1. Import master-seed.csv into Excel and save as master.xlsx. Import incoming.csv into a separate input workbook.
2. Launch Excel and read both sheets into data tables using their header rows as column names.
3. Build a list of existing RecordID values from the master data.
4. Create an exceptions sheet with RecordID and Reason headers.
5. Iterate over incoming records using For Each.
6. Trim required text fields, validate Department, and convert Amount with error handling. Reject invalid records.
7. Check whether RecordID already exists in the ID list. Reject duplicates.
8. For each accepted record, find the first free row in the master sheet and write RecordID, Name, Department, and Amount.
9. Add the written RecordID to the ID list, then continue.
10. Save the output workbook and close both Excel instances. Route file/open/write errors to a clear failure message rather than reporting success.

## Acceptance checks
- Compare the resulting master with expected-master.csv.
- Compare rejected IDs and reasons with expected-exceptions.csv.
- Confirm existing data and headers remain intact.
- Confirm duplicates inside the input batch are rejected.
- Confirm text Amount values are handled without stopping the flow.
- Rerun on the updated master: no accepted ID should be appended again. Exception results will differ because previously accepted records are now duplicates.
- Test an input sheet containing headers only: no master rows should change.

## Evidence to add after implementation
Add exported/copied PAD flow actions, screenshots of input/output and exceptions, and actual acceptance-check results.
