"""CLI entry: resolve GitHub domains and write hosts/hosts.json/README."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

from .domains import GITHUB_DOMAINS
from .formatter import format_hosts_block, format_hosts_json, now_iso_cn, render_readme
from .resolver import resolve_best_ip

ROOT = Path(__file__).resolve().parents[1]


def run(domains: list[str], output_dir: Path, template_path: Path) -> int:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "github-hosts/1.0 (+https://github.com/SatanKiss/github-hosts)",
            "Accept": "application/dns-json, application/json",
        }
    )

    results = []
    total = len(domains)
    for i, domain in enumerate(domains, 1):
        print(f"[{i}/{total}] resolving {domain} ...", flush=True)
        try:
            res = resolve_best_ip(domain, session)
        except Exception as e:
            print(f"  ! error: {e}", file=sys.stderr)
            from .resolver import ResolveResult

            res = ResolveResult(domain=domain, ip=None, latency_ms=None, source="error", candidates=[])
        results.append(res)
        status = f"{res.ip} ({res.latency_ms}ms, {res.source})" if res.ip else "unresolved"
        print(f"  -> {status}", flush=True)

    update_time = now_iso_cn()
    hosts_block = format_hosts_block(results, update_time)
    hosts_json = format_hosts_json(results, update_time)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "hosts").write_text(hosts_block, encoding="utf-8", newline="\n")
    (output_dir / "hosts.json").write_text(hosts_json, encoding="utf-8", newline="\n")

    if template_path.exists():
        readme = render_readme(template_path, hosts_block, update_time)
        (output_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")
        print(f"wrote {output_dir / 'README.md'}")
    else:
        print(f"template not found: {template_path}; skipped README", file=sys.stderr)

    print(f"wrote {output_dir / 'hosts'}")
    print(f"wrote {output_dir / 'hosts.json'}")
    resolved = sum(1 for r in results if r.ip)
    print(f"resolved {resolved}/{total} domains at {update_time}")
    return 0 if resolved else 2


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate merged GitHub hosts for acceleration.")
    p.add_argument("--output", "-o", default=str(ROOT), help="Output directory (default: project root)")
    p.add_argument(
        "--template",
        default=str(ROOT / "templates" / "README.template.md"),
        help="README template path",
    )
    p.add_argument("--domains-file", help="Optional file with extra domains (one per line)")
    args = p.parse_args(argv)

    domains = list(GITHUB_DOMAINS)
    if args.domains_file:
        extra = Path(args.domains_file).read_text(encoding="utf-8").splitlines()
        for line in extra:
            line = line.strip()
            if line and not line.startswith("#"):
                domains.append(line)
        domains = sorted(set(domains))

    return run(domains, Path(args.output), Path(args.template))


if __name__ == "__main__":
    raise SystemExit(main())
