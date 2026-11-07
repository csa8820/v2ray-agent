# v2ray-agent

- [感谢 JetBrains 提供的非商业开源软件开发授权](https://www.jetbrains.com/?from=v2ray-agent)


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/v2rayAgentChannel)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue)](https://t.me/technologyshare)
[![Official Website](https://img.shields.io/badge/Website-v2ray--agent.com-blue)](https://www.v2ray-agent.com/)
[![English Version](https://img.shields.io/badge/English-Version-blue)](documents/en/README_EN.md)

基于 Bash 的 Xray-core / sing-box 安装与管理脚本，支持普通主机部署和 Docker Reality 独立部署。

## 功能

*   **多核心支持:** 支持 Xray-core 和 sing-box，可按需安装单核心或组合使用.
*   **多协议支持:** 支持 VLESS（TLS、Reality、XHTTP）、VMess、Trojan、Hysteria2、Tuic、NaiveProxy、AnyTLS，以及独立 SOCKS5、Shadowsocks / SS2022 入站.
*   **TLS 与 Reality:** TLS 协议可通过 acme.sh 自动申请和续订证书；Reality 支持无域名部署.
*   **易于管理:** 提供菜单管理用户、端口、配置、核心版本、日志和证书，并支持二维码及客户端节点信息输出.
*   **订阅支持:** 生成和管理订阅链接，支持远程订阅配置.
*   **分流管理:** 提供 WARP/WireGuard（IPv4/IPv6）、IPv6、SOCKS5、DNS、VMess+WS、SNI 反向代理等分流能力，可用于流媒体等场景.
*   **网络策略管理:** 支持 Hysteria2 端口跳跃、域名黑名单和 BT/P2P 下载限制.
*   **Docker Reality:** 无需域名即可通过 Docker 部署 VLESS-Reality，支持 Vision、XHTTP 或同时启用两种模式，并提供交互式和命令行参数模式.
*   **更多内容请访问[官方网站](https://www.v2ray-agent.com/categories/jiao-cheng)、[备用](https://www.592083.com/categories/jiao-cheng)、[X](https://x.com/v2rayagent)**

## 环境要求

*   **脚本版:** Linux、root 权限，支持 CentOS、Debian、Ubuntu 和 Alpine；支持 amd64/x86_64、arm64/aarch64.
*   **Docker Reality:** Linux、root 或 sudo 权限，以及正在运行的 Docker；脚本可在交互模式下提示安装 Docker.

## 安装 Shadowsocks / SS2022

使用本修改版脚本，在 Linux 服务器以 root 身份运行 `bash install.sh`，选择主菜单 `19.Shadowsocks / SS2022 安装与管理`，再选择安装。英文入口为 `bash shell/install_en.sh`。

输入监听端口、加密方式和密码。端口默认 `8388`，密码留空会自动生成。可选加密方式包括 `aes-256-gcm`、`chacha20-ietf-poly1305`、`2022-blake3-aes-128-gcm` 和 `2022-blake3-aes-256-gcm`。SS2022 自定义密钥须为对应的 16 或 32 字节 Base64 编码，安装前会使用核心校验配置。

安装成功后会显示 `ss://` 链接和可放入 Clash / Mihomo `proxies` 列表的 JSON 节点对象。请在主机防火墙和云安全组放行所选端口的 TCP、UDP。服务监听 `::`，IPv4 可达性取决于系统的 IPv6 双栈设置。

菜单同时提供查看节点、重启和卸载 SS。配置保存在 `/etc/v2ray-agent/shadowsocks/config.json`，独立核心保存在同目录，服务名为 `v2ray-agent-ss`，支持 systemd 和 Alpine OpenRC。首次安装复用已有 sing-box 核心或项目的下载逻辑，后续重装复用独立核心。项目的核心升级菜单管理原有核心，SS 独立核心版本需自行维护。

SS 节点通过本菜单单独导出，项目的通用订阅与用户管理菜单暂未接入 SS。安装流程在发布前检查配置和端口，启动失败会恢复之前的配置、核心、服务定义及启用状态。主菜单的整体卸载会一并移除 SS。

此功能为本地修改。主菜单的更新脚本功能会从上游下载脚本，使用前请保留本修改版，避免更新后丢失 SS 菜单。

验证修改可运行 `bash -n install.sh`、`bash -n shell/install_en.sh` 和 `python3 -m unittest discover -s tests -v`，测试依赖 Bash、Python 3 和 jq。

## 快速开始

### 安装脚本版

```
wget -P /root -N --no-check-certificate "https://raw.githubusercontent.com/mack-a/v2ray-agent/master/install.sh" && chmod 700 /root/install.sh && /root/install.sh
```

### 使用

安装后，运行以下命令可再次打开管理菜单:

```
vasma
```

### 安装Docker版
```
wget -P /root -N --no-check-certificate "https://raw.githubusercontent.com/mack-a/v2ray-agent/master/shell/docker_reality.sh" && chmod 700 /root/docker_reality.sh && /root/docker_reality.sh
```

### 使用 

* [Docker Reality 使用说明](https://www.v2ray-agent.com/archives/019e1b57-92b3-70ab-8919-cdf8c0bb4fe9)
 
安装后，运行以下命令可再次打开管理菜单:

```
vasmad
```

## 文档和指南

*   [SOCKS5 入站与分流出站：简明教程](https://www.v2ray-agent.com/archives/01a1b212-d16c-743c-a4b1-d6150a948bda)

*   [八合一脚本从入门到精通](https://www.v2ray-agent.com/archives/1710141233)
*   [脚本快速搭建教程](https://www.v2ray-agent.com/archives/1682491479771)
*   [脚本使用注意事项](https://www.v2ray-agent.com/archives/1679931532764)
*   [脚本异常处理](https://www.v2ray-agent.com/archives/1684115970026)   
*   [VPS选购攻略](https://www.v2ray-agent.com/archives/1679975663984)
*   [垃圾VPS大救星，hysteria2最新协议一键搭建](https://www.v2ray-agent.com/archives/1697162969693)
*   [RackNerd低价 联通AS4837套餐，年付10美起](https://www.v2ray-agent.com/archives/racknerdtao-can-zheng-li-nian-fu-10mei-yuan)
*   [搬瓦工优质套餐推荐](https://www.v2ray-agent.com/archives/2023nian-ban-wa-gong-ji-fang-tui-jian)
*   [DMIT优质套餐推荐](https://www.v2ray-agent.com/archives/1679159868033)

## 社区与支持

*   **Telegram:** [频道](https://t.me/v2rayAgentChannel) | [群组](https://t.me/technologyshare)
*   **网站:** [官网](https://www.v2ray-agent.com/) | [备用](https://www.592083.xyz/)
*   **反馈:** [提交 issue](https://github.com/mack-a/v2ray-agent/issues)
*   **X:** [链接](https://x.com/v2rayagent)

## 捐赠

感谢您对开源项目的关注和支持。如果您觉得这个项目对您有帮助，欢迎通过以下方式进行捐赠。

*   [购买VPS捐赠](https://www.v2ray-agent.com/categories/vps)
*   [通过虚拟币向我捐赠](https://www.v2ray-agent.com/1679123834836)

## 许可证

本项根据 [AGPL-3.0 许可证](LICENSE) 授权.
