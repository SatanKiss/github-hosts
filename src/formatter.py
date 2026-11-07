"""Format hosts output and render templates."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from .resolver import ResolveResult

START_MARK = "# GitHub Host Start"
END_MARK = "# GitHub Host End"
PROJECT_URL = "https://github.com/SatanKiss/github-hosts"
HOSTS_URL_HINT = "https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts"
HOSTS_JSON_URL_HINT = "https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts.json"


def now_iso_cn() -> str:
    return (
        datetime.now(timezone.utc)
        .astimezone(timezone(timedelta(hours=8)))
        .replace(microsecond=0)
        .isoformat()
    )


def format_hosts_block(results: Iterable[ResolveResult], update_time: str) -> str:
    lines: list[str] = [START_MARK, ""]
    for r in results:
        if r.ip:
            comment = ""
            if r.latency_ms is None:
                comment = "  # timeout"
            lines.append(f"{r.ip.ljust(30)}{r.domain}{comment}")
        else:
            lines.append(f"{'# unresolved'.ljust(30)}{r.domain}")
    lines.extend(
        [
            "",
            f"# Update time: {update_time}",
            f"# Update url: {HOSTS_URL_HINT}",
            f"# Star: {PROJECT_URL}",
            END_MARK,
            "",
        ]
    )
    return "\n".join(lines)


def format_hosts_json(results: Iterable[ResolveResult], update_time: str) -> str:
    payload = {
        "update_time": update_time,
        "update_url": HOSTS_URL_HINT,
        "project": PROJECT_URL,
        "entries": [
            {
                "ip": r.ip,
                "domain": r.domain,
                "latency_ms": r.latency_ms,
                "source": r.source,
                "candidates": r.candidates,
            }
            for r in results
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_readme(template_path: Path, hosts_block: str, update_time: str) -> str:
    tpl = template_path.read_text(encoding="utf-8")
    return (
        tpl.replace("{hosts_block}", hosts_block.rstrip("\n"))
        .replace("{update_time}", update_time)
        .replace("{hosts_url}", HOSTS_URL_HINT)
        .replace("{hosts_json_url}", HOSTS_JSON_URL_HINT)
        .replace("{project_url}", PROJECT_URL)
    )
