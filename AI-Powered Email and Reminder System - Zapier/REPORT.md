# Project Report

**Title:** Smart Automated Email and Reminder System Using Zapier and CSV/Excel
**Course/Assignment:** Workflow Automation and Agentic AI, Assignment 1 (10 marks)
**Name / Roll No.:** ____________________  **Date:** ____________________

## 1. Aim
To build an automation that reads task information from a spreadsheet and sends personalised reminder emails on the correct date, without manual effort.

## 2. Tools Used
- Zapier (primary automation platform)
- Google Sheets (data source, imported from CSV)
- Gmail (email action)
- Code by Zapier (JavaScript, for validation and message building)

## 3. Dataset
A CSV of 10 records with the columns Name, Email, Task/Event, Due Date, Reminder Date and Status. Two helper columns were added in Google Sheets: `Email Sent` and `Send Today?`. The formula in `Send Today?` returns YES only when the reminder date is today, the status is Pending and no email has been sent.

## 4. Workflow
1. **Schedule by Zapier** starts the Zap every day.
2. **Lookup Spreadsheet Row** finds a row where `Send Today?` = YES.
3. **Code by Zapier** re-checks the rules, formats dates and builds the subject and body.
4. **Filter** continues only if the email should be sent.
5. **Gmail: Send Email** sends the reminder.
6. **Update Spreadsheet Row** writes `Sent` to prevent duplicates.

## 5. Scheduled vs New-Row Trigger
A scheduled trigger runs at a set time whether or not data changed. A new-row trigger runs only when a row is added. Reminders depend on the calendar date, so the scheduled trigger was chosen.

## 6. Duplicate Prevention and Safe Testing
Duplicates are prevented by the `Email Sent` marker, by the formula and Code-step checks, and by the Filter. Testing used only my own Gmail `+alias` addresses, with the Zap kept off until each step tested successfully.

## 7. Test Results
Fill this table from your own Zapier runs.

| Test | Expected | Actual (fill in) | Pass/Fail |
|---|---|---|---|
| T1 Reminder date is today | Email sent, G = Sent | | |
| T2 Re-run | No duplicate | | |
| T3 Status Done | No email | | |
| T4 No matching row | No email | | |
| T5 Different row | Correct personalisation | | |
| T6 Invalid email | No email | | |

The decision logic was also checked offline with a Python simulation (6 of 6 cases matched expectations). That simulation did not send any email.

## 8. Limitations
- Lookup Spreadsheet Row returns the first match, so one reminder per run unless a loop or line-item lookup is used.
- Free-plan task limits and polling intervals restrict volume and timing.
- Date formats in Sheets can break the formula if dates import as text.

## 9. Conclusion
The system sends scheduled, personalised reminders from spreadsheet data and avoids duplicates and invalid sends. It can be extended with SMS, Slack or a loop for multiple recipients.

## 10. Screenshots
Attach the screenshots from the checklist in `PROJECT_GUIDE.md` (section 9) here.
