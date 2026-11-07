"""Resolve domains to the best IP using multiple DNS sources and TCP probing."""

from __future__ import annotations

import asyncio
import socket
import sys
import time
from dataclasses import dataclass
from typing import Any

import requests

PING_TIMEOUT_SEC = 1.0
HTTPS_PORT = 443
TCP_PROBES = 3
DISCARD_IPS = {"1.0.1.1", "1.2.1.1", "127.0.0.1", "0.0.0.0"}

DOH_SERVERS = [
    ("https://dns.alidns.com/resolve", "alidns"),
    ("https://doh.pub/dns-query", "dnspod"),
    ("https://1.1.1.1/dns-query", "cloudflare-doh"),
    ("https://dns.google/resolve", "google-doh"),
]

DNS_SERVER_LIST = [
    "223.5.5.5",  # AliDNS
    "119.29.29.29",  # DNSPod
    "114.114.114.114",  # 114DNS
    "1.1.1.1",  # Cloudflare
    "8.8.8.8",  # Google
]


@dataclass
class ResolveResult:
    domain: str
    ip: str | None
    latency_ms: float | None
    source: str
    candidates: list[str]


_ping_cache: dict[str, float] = {}


def tcp_latency_ms(ip: str, port: int = HTTPS_PORT, timeout: float = PING_TIMEOUT_SEC) -> float:
    """Measure TCP connect latency (ms). Returns timeout*1000 on failure."""
    if ip in _ping_cache:
        return _ping_cache[ip]
    latencies: list[float] = []
    for _ in range(TCP_PROBES):
        try:
            start = time.perf_counter()
            with socket.create_connection((ip, port), timeout=timeout):
                latencies.append((time.perf_counter() - start) * 1000)
        except Exception:
            latencies.append(timeout * 1000)
    latencies.sort()
    # median
    median = latencies[len(latencies) // 2]
    _ping_cache[ip] = median
    return median


def get_ips_from_doh(domain: str, session: requests.Session) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for url, name in DOH_SERVERS:
        try:
            resp = session.get(
                url,
                params={"name": domain, "type": "A"},
                headers={"Accept": "application/dns-json"},
                timeout=5,
            )
            data = resp.json()
            if data.get("Status") == 0 and data.get("Answer"):
                for ans in data["Answer"]:
                    if ans.get("type") == 1 and ans.get("data"):
                        results.append((ans["data"], f"doh:{name}"))
        except Exception:
            continue
    return results


def _windows_event_loop_policy() -> None:
    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass


async def get_ips_from_dns(domain: str) -> list[tuple[str, str]]:
    """Query A records via UDP DNS using aiodns if available."""
    try:
        import aiodns  # type: ignore
    except Exception:
        # Fallback to system resolver (single answer)
        try:
            infos = socket.getaddrinfo(domain, None, family=socket.AF_INET)
            return [(info[4][0], "system") for info in infos]
        except Exception:
            return []

    resolver = aiodns.DNSResolver()
    resolver.nameservers = DNS_SERVER_LIST
    try:
        answers = await resolver.query(domain, "A")
        return [(a.host, "dns:udp") for a in answers]
    except Exception:
        return []


def _run_async(coro: Any) -> Any:
    _windows_event_loop_policy()
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # In rare embedded contexts; create a new loop in a thread-like fallback.
            new_loop = asyncio.new_event_loop()
            try:
                return new_loop.run_until_complete(coro)
            finally:
                new_loop.close()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


def resolve_best_ip(domain: str, session: requests.Session) -> ResolveResult:
    candidates: list[tuple[str, str]] = []
    candidates.extend(get_ips_from_doh(domain, session))
    candidates.extend(_run_async(get_ips_from_dns(domain)))

    # Dedupe while preserving source preference order roughly; keep all sources for debug.
    seen: set[str] = set()
    unique_ips: list[str] = []
    for ip, _src in candidates:
        if ip in DISCARD_IPS:
            continue
        if ip not in seen:
            seen.add(ip)
            unique_ips.append(ip)

    if not unique_ips:
        return ResolveResult(domain=domain, ip=None, latency_ms=None, source="none", candidates=[])

    timeout_ms = PING_TIMEOUT_SEC * 1000
    scored: list[tuple[float, str]] = [(tcp_latency_ms(ip), ip) for ip in unique_ips]
    scored.sort(key=lambda x: x[0])

    # Prefer reachable candidates. Writing an unreachable IP into hosts causes
    # browsers/tools to hang on TCP connect, which is worse than leaving the
    # domain to system DNS. If every candidate times out, mark as unresolved.
    reachable = [(lat, ip) for lat, ip in scored if lat < timeout_ms]
    if not reachable:
        return ResolveResult(
            domain=domain,
            ip=None,
            latency_ms=None,
            source="timeout",
            candidates=unique_ips,
        )

    best_latency, best_ip = reachable[0]

    # Determine a representative source for the chosen IP.
    source = "mixed"
    for ip, src in candidates:
        if ip == best_ip:
            source = src
            break

    return ResolveResult(
        domain=domain,
        ip=best_ip,
        latency_ms=round(best_latency, 2),
        source=source,
        candidates=unique_ips,
    )
