# github-hosts

合并 [GitHub520](https://github.com/521xueweihan/GitHub520) 与 [ineo6/hosts](https://github.com/ineo6/hosts) 思路的 GitHub Hosts 加速项目，目标是**尽可能覆盖 GitHub 相关访问**，并支持通过 **URL 方式直接引入 hosts**。

> 数据可由 GitHub Actions 自动更新。示例更新时间：**2026-11-07T11:59:32+08:00**

## 一、通过 URL 引入（推荐）

将下面任一 URL 配置到支持“远程 hosts / 订阅规则”的工具中，即可自动获取最新内容。

| 用途 | URL |
|---|---|
| Hosts 文本（主地址） | `https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts` |
| JSON 数据 | `https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts.json` |
| jsDelivr CDN | `https://cdn.jsdelivr.net/gh/SatanKiss/github-hosts@main/hosts` |
| jsDelivr JSON | `https://cdn.jsdelivr.net/gh/SatanKiss/github-hosts@main/hosts.json` |

### SwitchHosts 配置示例

- 类型：`Remote`
- 标题：`github-hosts`
- URL：`https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts`（或 jsDelivr 地址）
- 自动刷新：`1 小时`

### AdGuard Home / AdGuard DNS 规则

在支持 hosts 列表订阅的位置添加：`https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts`（具体入口因版本不同而异）。

## 二、手动方式

复制下方 hosts 内容，追加/替换到系统 hosts 文件中对应 `# GitHub Host Start` / `# GitHub Host End` 区块。

```bash
# GitHub Host Start

# unresolved                  actions.githubusercontent.com
140.82.112.26                 alive.github.com
20.205.243.168                api.github.com
140.82.114.22                 api.githubcopilot.com
140.82.114.22                 api.individual.githubcopilot.com
# unresolved                  assets-cdn.github.com
185.199.108.133               avatars.githubusercontent.com
185.199.108.133               avatars0.githubusercontent.com
185.199.108.133               avatars1.githubusercontent.com
185.199.108.133               avatars2.githubusercontent.com
185.199.108.133               avatars3.githubusercontent.com
185.199.108.133               avatars4.githubusercontent.com
185.199.108.133               avatars5.githubusercontent.com
185.199.108.133               camo.githubusercontent.com
140.82.112.21                 central.github.com
185.199.108.133               cloud.githubusercontent.com
20.205.243.165                codeload.github.com
140.82.113.21                 collector.github.com
140.82.113.21                 collector.githubapp.com
4.249.131.160                 copilot-proxy.githubusercontent.com
185.199.108.133               copilot.githubusercontent.com
13.107.5.93                   default.exp-tas.com
185.199.108.133               desktop.githubusercontent.com
185.199.109.154               docs.github.com
140.82.113.21                 education.github.com
185.199.108.133               favicons.githubusercontent.com
20.205.243.164                ghcr.io
20.205.243.166                gist.github.com
52.216.32.138                 github-cloud.s3.amazonaws.com
16.182.66.122                 github-com.s3.amazonaws.com
52.217.226.226                github-production-release-asset-2e65be.s3.amazonaws.com
54.231.129.130                github-production-repository-file-5c1aeb.s3.amazonaws.com
52.217.135.186                github-production-user-asset-6210df.s3.amazonaws.com
192.0.66.2                    github.blog
20.205.243.166                github.com
140.82.112.18                 github.community
20.43.185.14                  github.dev
185.199.108.215               github.githubassets.com
# timeout                     github.global.ssl.fastly.net
185.199.111.153               github.io
185.199.108.133               github.map.fastly.net
140.82.113.29                 githubapp.com
185.199.111.153               githubstatus.com
# unresolved                  graphql.github.com
140.82.114.26                 live.github.com
185.199.108.133               media.githubusercontent.com
140.82.114.22                 models.github.ai
20.205.243.164                npm.pkg.github.com
185.199.108.133               objects.githubusercontent.com
140.82.114.22                 origin-tracker.githubusercontent.com
13.107.42.16                  pipelines.actions.githubusercontent.com
185.199.109.154               pkg-containers.githubusercontent.com
20.205.243.164                pkg.github.com
185.199.108.133               private-user-images.githubusercontent.com
4.249.131.160                 proxy.enterprise.githubcopilot.com
# unresolved                  proxy.githubcopilot.com
185.199.108.133               raw.github.com
185.199.108.133               raw.githubusercontent.com
104.21.60.54                  rawcdn.githack.com
185.199.108.133               support.github.com
# unresolved                  tunnels.api.visualstudio.com
20.205.243.161                uploads.github.com
185.199.108.133               user-images.githubusercontent.com
185.199.111.153               vscode-auth.github.com
150.171.110.106               vscode.dev

# Update time: 2026-11-07T11:59:32+08:00
# Update url: https://raw.githubusercontent.com/SatanKiss/github-hosts/main/hosts
# Star: https://github.com/SatanKiss/github-hosts
# GitHub Host End
```

### hosts 文件位置

- Windows：`C:\Windows\System32\drivers\etc\hosts`
- Linux / macOS：`/etc/hosts`

### 刷新 DNS

- Windows：`ipconfig /flushdns`
- macOS：`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- Linux（systemd-resolved）：`sudo resolvectl flush-caches`

## 三、覆盖范围

本项目合并两源域名清单，并补充常见 GitHub/Copilot/Packages/Actions/VSCode 相关域名，解析时综合使用：

- DoH（阿里 DNS / DNSPod / Cloudflare / Google）
- UDP DNS（多国内/国际服务器，依赖环境）
- 对候选 IP 做 TCP 443 连接测速，优先选择可达且延迟更低的地址

> Hosts 加速受网络环境、运营商、CDN 调度影响，不保证所有地区/时刻均有效。若某条目解析失败，会保留为 `# unresolved`，避免写入错误地址。

## 四、本地生成

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

生成文件：`hosts`、`hosts.json`、`README.md`。

## 五、自动更新

仓库内置 [`.github/workflows/update-hosts.yml`](.github/workflows/update-hosts.yml)，默认每 2 小时运行一次并在内容变化时提交。Fork 后在仓库 Actions 中启用即可。

## 六、来源与许可说明

- 域名覆盖与实现思路参考了 [GitHub520](https://github.com/521xueweihan/GitHub520)（原项目声明为 CC BY-NC-ND 4.0）与 [ineo6/hosts](https://github.com/ineo6/hosts)（MIT）。本合并仓库为重新组织的工程实现；发布前请确认你对原项目内容/许可的使用符合其条款，并根据需要补充完整许可证文本与署名。
- 本项目生成的 hosts 数据仅用于网络可达性优化，请遵守当地法律法规及相关服务条款。

## Star

如果有帮助，欢迎 Star：https://github.com/SatanKiss/github-hosts
