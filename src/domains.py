"""GitHub acceleration domain catalog.

Merged from GitHub520 and ineo6/hosts, with additional common GitHub-related
domains to maximize acceleration coverage.
"""

from __future__ import annotations

# Core domains merged from both projects + common GitHub acceleration targets.
# Keep entries unique and stable-sorted by hostname.
GITHUB_DOMAINS: list[str] = sorted(
    set(
        [
            # --- GitHub520 domains ---
            "alive.github.com",
            "api.github.com",
            "api.individual.githubcopilot.com",
            "avatars.githubusercontent.com",
            "avatars0.githubusercontent.com",
            "avatars1.githubusercontent.com",
            "avatars2.githubusercontent.com",
            "avatars3.githubusercontent.com",
            "avatars4.githubusercontent.com",
            "avatars5.githubusercontent.com",
            "camo.githubusercontent.com",
            "central.github.com",
            "cloud.githubusercontent.com",
            "codeload.github.com",
            "collector.github.com",
            "desktop.githubusercontent.com",
            "education.github.com",
            "favicons.githubusercontent.com",
            "gist.github.com",
            "github-cloud.s3.amazonaws.com",
            "github-com.s3.amazonaws.com",
            "github-production-release-asset-2e65be.s3.amazonaws.com",
            "github-production-repository-file-5c1aeb.s3.amazonaws.com",
            "github-production-user-asset-6210df.s3.amazonaws.com",
            "github.blog",
            "github.com",
            "github.community",
            "github.dev",
            "github.githubassets.com",
            "github.global.ssl.fastly.net",
            "github.io",
            "github.map.fastly.net",
            "githubstatus.com",
            "live.github.com",
            "media.githubusercontent.com",
            "objects.githubusercontent.com",
            "pipelines.actions.githubusercontent.com",
            "private-user-images.githubusercontent.com",
            "raw.githubusercontent.com",
            "user-images.githubusercontent.com",
            "vscode.dev",
            # --- ineo6/hosts additions ---
            "assets-cdn.github.com",
            "copilot-proxy.githubusercontent.com",
            "raw.github.com",
            # --- Additional common acceleration targets ---
            "actions.githubusercontent.com",
            "api.githubcopilot.com",
            "collector.githubapp.com",
            "copilot.githubusercontent.com",
            "default.exp-tas.com",
            "docs.github.com",
            "ghcr.io",
            "githubapp.com",
            "graphql.github.com",
            "models.github.ai",
            "npm.pkg.github.com",
            "origin-tracker.githubusercontent.com",
            "pkg-containers.githubusercontent.com",
            "pkg.github.com",
            "proxy.enterprise.githubcopilot.com",
            "proxy.githubcopilot.com",
            "rawcdn.githack.com",
            "support.github.com",
            "tunnels.api.visualstudio.com",
            "uploads.github.com",
            "vscode-auth.github.com",
        ]
    )
)

# Domains that are known to be CDN/CNAME-heavy and may benefit from extra
# resolution attempts; kept for future heuristics.
CDN_HINT_DOMAINS: set[str] = {
    "github.global.ssl.fastly.net",
    "github.map.fastly.net",
}
