# github-host

合并 [GitHub520](https://github.com/521xueweihan/GitHub520) 与 [ineo6/hosts](https://github.com/ineo6/hosts) 思路的 GitHub Hosts 加速项目，目标是**尽可能覆盖 GitHub 相关访问**，并支持通过 **URL 方式直接引入 hosts**。

> 数据自动更新（GitHub Actions）。最近更新时间：**{update_time}**

## 一、通过 URL 引入（推荐）

将下面任一 URL 配置到支持“远程 hosts / 订阅规则”的工具中，即可自动获取最新内容。

| 用途 | URL |
|---|---|
| Hosts 文本（主地址） | `{hosts_url}` |
| JSON 数据 | `{hosts_json_url}` |
| jsDelivr CDN | `https://cdn.jsdelivr.net/gh/SatanKiss/github-hosts@main/hosts` |
| jsDelivr JSON | `https://cdn.jsdelivr.net/gh/SatanKiss/github-hosts@main/hosts.json` |

### SwitchHosts 配置示例

- 类型：`Remote`
- 标题：`github-host`
- URL：`{hosts_url}`（或 jsDelivr 地址）
- 自动刷新：`1 小时`

### AdGuard Home / AdGuard DNS 规则

在支持 hosts 列表订阅的位置添加：`{hosts_url}`（具体入口因版本不同而异）。

## 二、手动方式

复制下方 hosts 内容，追加/替换到系统 hosts 文件中对应 `# GitHub Host Start` / `# GitHub Host End` 区块。

```bash
{hosts_block}
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

如果有帮助，欢迎 Star：{project_url}
