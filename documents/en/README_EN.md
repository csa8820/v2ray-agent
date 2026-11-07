# v2ray-agent

This fork is [csa8820/v2ray-agent](https://github.com/csa8820/v2ray-agent), based on [mack-a/v2ray-agent](https://github.com/mack-a/v2ray-agent), with standalone Shadowsocks / SS2022 installation and management. Script updates and project assets use this fork’s `master` branch.

- [Thanks to JetBrains for providing non-commercial open source software development authorization](https://www.jetbrains.com/?from=v2ray-agent)


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/v2rayAgentChannel)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue)](https://t.me/technologyshare)
[![Official Website](https://img.shields.io/badge/Website-v2ray--agent.com-blue)](https://www.v2ray-agent.com/)
[![English Version](https://img.shields.io/badge/English-Version-blue)](README_EN.md)

An installation and management script for Xray-core and sing-box, with regular host deployment and standalone Docker Reality deployment.

## Features

*   **Multi-core Support:** Supports Xray-core and sing-box, either separately or in combination.
*   **Multi-protocol Support:** Supports VLESS (TLS, Reality, XHTTP), VMess, Trojan, Hysteria2, Tuic, NaiveProxy, AnyTLS, and standalone SOCKS5 inbound.
*   **TLS and Reality:** TLS protocols can use acme.sh for automatic certificate issuance and renewal; Reality supports deployment without a domain.
*   **Easy Management:** Provides menus for users, ports, configurations, core versions, logs, and certificates, with QR codes and client node output.
*   **Subscription Support:** Generates and manages subscription links, including remote subscription configuration.
*   **Traffic Routing:** Provides WARP/WireGuard (IPv4/IPv6), IPv6, SOCKS5, DNS, VMess+WS, and SNI reverse-proxy routing.
*   **Network Policy Management:** Supports Hysteria2 port hopping, domain blacklists, and BT/P2P download restrictions.
*   **Docker Reality:** Runs VLESS-Reality in Docker without a domain, with Vision, XHTTP, or combined modes and both interactive and CLI operation.
*   **For more content, please visit the [Official Website](https://www.v2ray-agent.com/categories/jiao-cheng), [Backup](https://www.592083.com/categories/jiao-cheng)**

## Requirements

*   **Regular installation:** Linux with root privileges; CentOS, Debian, Ubuntu, and Alpine are supported on amd64/x86_64 and arm64/aarch64.
*   **Docker Reality:** Linux with root or sudo privileges and a running Docker daemon; the script can offer to install Docker interactively.

## Quick Start

### Installation

```
curl -fL -o /root/install.sh https://raw.githubusercontent.com/csa8820/v2ray-agent/master/shell/install_en.sh && chmod 700 /root/install.sh && bash /root/install.sh
```

### Shadowsocks / SS2022

As root on Linux, run the installation command above, then select main menu `19` and option `1`. Choose a port, cipher and password. An empty password generates a random credential. The result includes an `ss://` link and a Clash / Mihomo node object. Allow the selected TCP and UDP port in the host firewall and cloud security group.

Menu `19` also shows credentials, restarts SS and uninstalls SS. Configuration lives in `/etc/v2ray-agent/shadowsocks/config.json`; the independent service is `v2ray-agent-ss`. SS nodes are exported separately from the general subscription and user management menus. Main menu `17` updates the script from this fork.

### Usage

After installation, run the following command to open the management menu again:

```
vasma
```

### Docker Reality

```
wget -P /root -N --no-check-certificate "https://raw.githubusercontent.com/csa8820/v2ray-agent/master/shell/docker_reality_en.sh" && chmod 700 /root/docker_reality_en.sh && /root/docker_reality_en.sh
```

The Docker launcher supports Reality Vision, Reality XHTTP, or both modes. After installation, run `vasmad` to reopen its menu. See the [Docker Reality guide](https://www.v2ray-agent.com/archives/019e1b57-92b3-70ab-8919-cdf8c0bb4fe9).

## Documentation and Guides

*   [From Beginner to Master with the 8-in-1 Script](https://www.v2ray-agent.com/archives/1710141233)
*   [Quick Script Setup Tutorial](https://www.v2ray-agent.com/archives/1682491479771)
*   [Script Usage Precautions](https://www.v2ray-agent.com/archives/1679931532764)
*   [Script Exception Handling](https://www.v2ray-agent.com/archives/1684115970026)   
*   [VPS Purchasing Guide](https://www.v2ray-agent.com/archives/1679975663984)
*   [Junk VPS Savior, one-click setup of the latest hysteria2 protocol](https://www.v2ray-agent.com/archives/1697162969693)
*   [RackNerd Low-cost Unicom AS4837 Package, starting from $10/year](https://www.v2ray-agent.com/archives/racknerdtao-can-zheng-li-nian-fu-10mei-yuan)
*   [Recommended High-Quality Bandwagon Host Packages](https://www.v2ray-agent.com/archives/2023nian-ban-wa-gong-ji-fang-tui-jian)
*   [Recommended High-Quality DMIT Packages](https://www.v2ray-agent.com/archives/1679159868033)

## Community & Support

*   **Telegram:** [Channel](https://t.me/v2rayAgentChannel) | [Group](https://t.me/technologyshare)
*   **Website:** [Official](https://www.v2ray-agent.com/) | [Backup](https://www.592083.xyz/)
*   **Feedback:** [Submit an issue](https://github.com/csa8820/v2ray-agent/issues)
*   **X:** [Link](https://x.com/v2rayagent)

## Donation

Thank you for your attention and support for this open source project. If you find this project helpful, you are welcome to donate in the following ways.

*   [Donate by purchasing a VPS](https://www.v2ray-agent.com/categories/vps)
*   [Donate to me via cryptocurrency](https://www.v2ray-agent.com/1679123834836)

## License

This project is licensed under the [AGPL-3.0 License](LICENSE).
