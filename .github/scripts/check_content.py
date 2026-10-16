"""Content checks for CMS edits, run by .github/workflows/site-check.yml.

Errors fail the run (GitHub emails the editor); warnings are shown on the
commit and in the run summary. Also decides whether a scheduled rebuild is due.
"""
import csv
import io
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Australia/Hobart")
# Matches the hourly cron, with slack for late-starting scheduled runs.
DUE_WINDOW = timedelta(minutes=90)

errors, warnings = [], []


def annotate(level, path, msg):
    print(f"::{level} file={path}::{msg}")
    (errors if level == "error" else warnings).append(f"`{path}`: {msg}")


def body_of(path):
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    parts = text.split("---\n", 2)
    body = parts[2] if len(parts) == 3 else text
    return re.sub(r"\s+", " ", body).strip().lower()


def parse(value):
    if not value or value.startswith("0001-01-01"):
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


rows = list(csv.DictReader(io.StringIO(
    subprocess.run(["hugo", "list", "all"], check=True,
                   capture_output=True, text=True).stdout)))
now = datetime.now(timezone.utc)
due = False
by_body = defaultdict(list)
by_title = defaultdict(list)

for row in rows:
    if row["kind"] != "page":
        continue
    path, title = row["path"], row["title"]
    draft = row["draft"] == "true"
    published = parse(row["publishDate"]) or parse(row["date"])

    if draft:
        annotate("notice", path, f'"{title}" is a draft and is hidden from the site.')
    elif published and published > now:
        local = published.astimezone(TZ).strftime("%-d %b %Y, %-I:%M %p")
        annotate("warning", path,
                 f'"{title}" is dated {local} (Tasmanian time), so it stays hidden '
                 "until then. If it should be visible now, change its date in the CMS.")
    elif published and now - published <= DUE_WINDOW:
        due = True

    if not draft and row["section"] in ("news", "events", "documents"):
        by_body[(row["section"], body_of(path))].append(path)
        by_title[(row["section"], title.strip().lower())].append(path)

for (section, body), paths in by_body.items():
    if body and len(paths) > 1:
        for path in paths:
            annotate("error", path,
                     f"Duplicate {section} entry: same text as {', '.join(p for p in paths if p != path)}. "
                     "Delete the extra copy in the CMS (edit the existing entry instead of creating a new one).")

for (section, _), paths in by_title.items():
    if len(paths) > 1:
        for path in paths:
            annotate("warning", path,
                     f"Another {section} entry has the same title: {', '.join(p for p in paths if p != path)}.")

# Once a day (around midnight Tasmanian time) rebuild anyway so the
# upcoming/past event lists move on.
if datetime.now(TZ).hour == 0:
    due = True

summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as f:
        f.write("## Content check\n\n")
        for label, items in (("Errors", errors), ("Warnings", warnings)):
            if items:
                f.write(f"### {label}\n" + "".join(f"- {i}\n" for i in items) + "\n")
        if not errors and not warnings:
            f.write("No problems found.\n")

output = os.environ.get("GITHUB_OUTPUT")
if output:
    with open(output, "a") as f:
        f.write(f"rebuild={'true' if due else 'false'}\n")

sys.exit(1 if errors else 0)
