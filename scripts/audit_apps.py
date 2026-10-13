import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml


def get_installations(organization, token, per_page=100):
    installations = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/orgs/{quote(organization, safe='')}/installations"
            f"?per_page={per_page}&page={page}"
        )
        request = Request(
            url,
            method="GET",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2026-03-10",
                "User-Agent": "github-app-governance-audit",
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                items = json.load(response)["installations"]
        except HTTPError as error:
            raise RuntimeError(f"GitHub inventory request returned HTTP {error.code}.") from None
        except URLError:
            raise RuntimeError("GitHub inventory request failed.") from None
        installations.extend(items)
        if len(items) < per_page:
            return installations
        page += 1


def audit(catalog, installations, today):
    findings = []
    managed = {}
    for name, app in catalog["apps"].items():
        installation_id = str(app["installation_id"])
        if installation_id in managed:
            findings.append(f"Duplicate installation ID: {installation_id}.")
        managed[installation_id] = name
        for field in ("owner", "purpose"):
            value = app.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(f"{name}: {field} is missing or empty.")
        try:
            review_due = date.fromisoformat(str(app.get("review_due", "")))
        except ValueError:
            findings.append(f"{name}: review_due must be a valid ISO date.")
        else:
            if review_due <= today:
                findings.append(f"{name}: review due {review_due} (owner: {app.get('owner', 'missing')}).")

    live = {str(installation["id"]): installation for installation in installations}
    for installation_id, installation in live.items():
        if installation_id not in managed:
            findings.append(
                f"Unmanaged App: {installation['app_slug']} (installation {installation_id})."
            )
        elif installation["repository_selection"] != "selected":
            findings.append(f"{managed[installation_id]}: installation uses all-repository access.")
    for installation_id, name in managed.items():
        if installation_id not in live:
            findings.append(f"{name}: catalog installation {installation_id} is missing from GitHub.")
    return findings


def main():
    parser = argparse.ArgumentParser(description="Report unmanaged GitHub Apps and overdue reviews.")
    parser.add_argument("--catalog", default="config/apps.yaml")
    parser.add_argument("--report-file", help="Write the Markdown report for publishing.")
    args = parser.parse_args()
    checked_at = datetime.now(timezone.utc)
    try:
        token = os.environ.get("GITHUB_TOKEN", "").strip()
        if not token or not token.isascii() or any(character.isspace() for character in token):
            raise RuntimeError("Set a valid GITHUB_TOKEN securely in the environment.")
        catalog = yaml.safe_load(Path(args.catalog).read_text(encoding="utf-8"))
        installations = get_installations(catalog["organization"], token)
        today = checked_at.date()
        findings = audit(catalog, installations, today)
        report = (
            f"## GitHub App audit: {catalog['organization']}\n\n"
            f"{len(installations)} live installations; {len(catalog['apps'])} catalog entries.\n\n"
        )
        report += "\n".join(f"- {finding}" for finding in findings) if findings else "No findings."
        exit_code = 1 if findings else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, RuntimeError, yaml.YAMLError) as error:
        report = f"## GitHub App audit failed\n\n{error}"
        exit_code = 2
    report += f"\n\nChecked: {checked_at:%Y-%m-%d %H:%M:%S UTC}."
    if args.report_file:
        Path(args.report_file).write_text(report + "\n", encoding="utf-8")
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as file:
            file.write(report + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
