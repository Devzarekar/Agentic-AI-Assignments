"""
Local DRY-RUN tester for the Reminder System logic.

IMPORTANT: This script NEVER sends email and never talks to Zapier.
It only checks that the filtering and duplicate-prevention rules give the
expected results on reminders.csv, so you can trust the Zap before you
turn it on. Real proof of sending must come from YOUR Zapier account.

Run:  python3 dry_run_test.py
"""
import csv
import re
import sys
from datetime import date, datetime
from pathlib import Path

CSV_FILE = Path(__file__).with_name("reminders.csv")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def load_rows():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["Email Sent"] = ""  # the extra column you add in Google Sheets
    return rows


def parse(d):
    return datetime.strptime(d, "%Y-%m-%d").date()


def send_today(row, today):
    """Same rule as the sheet formula in column H."""
    return (
        EMAIL_RE.match(row["Email"]) is not None
        and parse(row["Reminder Date"]) == today
        and row["Status"].strip() == "Pending"
        and row["Email Sent"].strip() != "Sent"
    )


def build_email(row, today):
    due = parse(row["Due Date"])
    days_left = (due - today).days
    subject = f"Reminder: {row['Task/Event']} is due on {due.strftime('%d %b %Y')}"
    body = (
        f"Hi {row['Name']},\n\n"
        f"This is a friendly reminder that \"{row['Task/Event']}\" is due on "
        f"{due.strftime('%d %b %Y')} ({days_left} day(s) left).\n\n"
        f"Current status: {row['Status']}\n\n"
        "Please complete it before the deadline.\n\n"
        "Regards,\nAutomated Reminder System\n(Sent via Zapier)"
    )
    return subject, body


def run_day(rows, today, mark_sent=True):
    """Simulates one daily Zap run. Returns the names that WOULD get mail."""
    would_send = []
    for r in rows:
        if send_today(r, today):
            would_send.append(r["Name"])
            if mark_sent:
                r["Email Sent"] = "Sent"  # Zap step 5
    return would_send


def check(label, actual, expected):
    ok = actual == expected
    print(f"[{'PASS' if ok else 'FAIL'}] {label}\n        expected={expected} actual={actual}")
    return ok


def main():
    results = []

    # Test 1: reminder date = today, Pending -> exactly one reminder
    rows = load_rows()
    d1 = date(2026, 10, 10)
    results.append(check("T1 Reminder date is today & Pending -> sends",
                         run_day(rows, d1), ["Aarav Patil"]))

    # Test 2: run again same day -> duplicate prevented
    results.append(check("T2 Re-run same day -> no duplicate",
                         run_day(rows, d1), []))

    # Test 3: Status Done on its reminder date -> no email
    rows = load_rows()
    results.append(check("T3 Status Done on reminder date -> no email",
                         run_day(rows, date(2026, 10, 11)), []))

    # Test 4: no row matches the day -> nothing sent
    rows = load_rows()
    results.append(check("T4 No matching row -> nothing sent",
                         run_day(rows, date(2026, 10, 9)), []))

    # Test 5: another date -> correct person selected
    rows = load_rows()
    results.append(check("T5 Date 2026-10-14 -> Rohan only",
                         run_day(rows, date(2026, 10, 14)), ["Rohan Deshmukh"]))

    # Test 6: invalid email is skipped
    rows = load_rows()
    rows[0]["Email"] = "not-an-email"
    results.append(check("T6 Invalid email -> skipped",
                         run_day(rows, d1), []))

    # Show the email that would be built for the Test 1 row
    rows = load_rows()
    subject, body = build_email(rows[0], d1)
    print("\n--- Sample email preview (NOT sent) ---")
    print("To:     ", rows[0]["Email"])
    print("Subject:", subject)
    print(body)

    passed = sum(results)
    print(f"\n{passed}/{len(results)} logic tests passed.")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
