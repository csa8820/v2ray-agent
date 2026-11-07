"""Exercise the SS menu helpers without installing services or changing /etc."""
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class ShadowsocksTests(unittest.TestCase):
    script = "install.sh"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.managed = self.root / "agent/shadowsocks"
        self.managed.mkdir(parents=True)
        source = (REPO / self.script).read_text()
        start = source.index("# Standalone Shadowsocks uses")
        self.functions = source[start:source.index("\nmenu() {", start)]
        self.functions = self.functions.replace("/etc/v2ray-agent", str(self.root / "agent"))
        self.functions = self.functions.replace("/etc/systemd/system/v2ray-agent-ss.service", str(self.root / "ss.service"))
        self.functions = self.functions.replace("/etc/init.d/v2ray-agent-ss", str(self.root / "ss.openrc"))
        self.helpers = r'''
release=debian
echoContent() { printf '%s\n' "$2" >&2; }
prepareSingBoxCoreForSocks5() {
    mkdir -p "$SS_TEST_ROOT/agent/sing-box"
    cat >"$SS_TEST_ROOT/agent/sing-box/sing-box" <<'CORE'
#!/bin/bash
[[ ! -f "$SS_TEST_ROOT/fail-check" ]] || exit 1
jq -e '.inbounds[0].type == "shadowsocks"' "$3" >/dev/null
CORE
    chmod 755 "$SS_TEST_ROOT/agent/sing-box/sing-box"
}
shadowsocksService() {
    case "$1" in
    active) [[ -f "$SS_TEST_ROOT/active" ]] ;;
    enabled) [[ -f "$SS_TEST_ROOT/enabled" ]] ;;
    start|restart)
        if [[ -f "$SS_TEST_ROOT/fail-start" ]] &&
            jq -e '.inbounds[0].listen_port == 9001' "$SS_TEST_ROOT/agent/shadowsocks/config.json" >/dev/null; then return 1; fi
        touch "$SS_TEST_ROOT/active" ;;
    stop) rm -f "$SS_TEST_ROOT/active" ;;
    enable) touch "$SS_TEST_ROOT/enabled" ;;
    disable) rm -f "$SS_TEST_ROOT/enabled" ;;
    pid) printf '123\n' ;;
    reload) return 0 ;;
    esac
}
lsof() {
    if [[ " $* " == *' -p '* ]]; then [[ -f "$SS_TEST_ROOT/active" ]]
    else [[ -f "$SS_TEST_ROOT/occupied" ]] && printf "456\n"; fi
}
'''

    def run_shell(self, command, success=True):
        result = subprocess.run(
            ["bash", "-c", self.functions + self.helpers + command],
            env={**os.environ, "SS_TEST_ROOT": str(self.root)},
            text=True, capture_output=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def install(self, port=8388):
        return self.run_shell(f'''
shadowsocksGenerateConfig {port} aes-256-gcm 'test-password' >"$SS_TEST_ROOT/candidate.json" &&
shadowsocksApply install "$SS_TEST_ROOT/candidate.json"
''')

    def test_supported_ciphers_and_quoted_password(self):
        for method in ("aes-128-gcm", "aes-256-gcm", "chacha20-ietf-poly1305"):
            result = self.run_shell(f"shadowsocksGenerateConfig 08388 {method} 'a\"b\\c'")
            inbound = json.loads(result.stdout)["inbounds"][0]
            self.assertEqual(inbound["listen_port"], 8388)
            self.assertEqual(inbound["password"], 'a"b\\c')
        for size in (16, 32):
            key = base64.b64encode(bytes(size)).decode()
            self.run_shell(f"shadowsocksGenerateConfig 65535 2022-blake3-aes-{size * 8}-gcm '{key}'")

    def test_invalid_inputs(self):
        for port in ("0", "65536", "-1", "1.5", "abc"):
            self.run_shell(f"shadowsocksGenerateConfig '{port}' aes-256-gcm pass", success=False)
        self.run_shell("shadowsocksGenerateConfig 8388 invalid pass", success=False)
        self.run_shell("shadowsocksGenerateConfig 8388 2022-blake3-aes-128-gcm short", success=False)

    def test_install_and_remove(self):
        unrelated = self.root / "unrelated.json"
        unrelated.write_text("keep")
        self.install()
        self.assertTrue((self.root / "enabled").exists())
        self.assertEqual((self.managed / "config.json").stat().st_mode & 0o777, 0o600)
        self.run_shell("shadowsocksApply remove")
        self.assertFalse((self.managed / "config.json").exists())
        self.assertFalse((self.root / "ss.service").exists())
        self.assertEqual(unrelated.read_text(), "keep")

    def test_install_through_menu(self):
        result = self.run_shell('''
installSocks5InboundTools() { return 0; }
getPublicIP() { printf '192.0.2.1'; }
shadowsocksMenu <<'INPUT'
1
8388
1
test-password
INPUT
''')
        self.assertIn("ss://", result.stdout)
        self.assertTrue((self.root / "active").exists())

    def test_openrc_service(self):
        self.run_shell('''
release=alpine
shadowsocksGenerateConfig 8388 aes-256-gcm pass >"$SS_TEST_ROOT/candidate.json" &&
shadowsocksApply install "$SS_TEST_ROOT/candidate.json" &&
bash -n "$SS_TEST_ROOT/ss.openrc" && shadowsocksApply remove
''')
        self.assertFalse((self.root / "ss.openrc").exists())

    def test_failed_first_install_removes_partial_state(self):
        (self.root / "fail-start").touch()
        self.run_shell('''
shadowsocksGenerateConfig 9001 aes-256-gcm pass >"$SS_TEST_ROOT/candidate.json" &&
shadowsocksApply install "$SS_TEST_ROOT/candidate.json"
''', success=False)
        self.assertFalse((self.managed / "config.json").exists())
        self.assertFalse((self.managed / "sing-box").exists())
        self.assertFalse((self.root / "ss.service").exists())
        self.assertFalse((self.root / "enabled").exists())

    def test_failed_reinstall_restores_old_service(self):
        self.install()
        config = (self.managed / "config.json").read_bytes()
        unit = (self.root / "ss.service").read_bytes()
        (self.root / "fail-start").touch()
        self.run_shell('''
shadowsocksGenerateConfig 9001 aes-256-gcm replacement >"$SS_TEST_ROOT/new.json" &&
shadowsocksApply install "$SS_TEST_ROOT/new.json"
''', success=False)
        self.assertEqual((self.managed / "config.json").read_bytes(), config)
        self.assertEqual((self.root / "ss.service").read_bytes(), unit)
        self.assertTrue((self.root / "active").exists())
        self.assertTrue((self.root / "enabled").exists())
        self.assertFalse((self.managed / ".lock").exists())

    def test_validation_failure_leaves_running_service(self):
        self.install()
        config = (self.managed / "config.json").read_bytes()
        (self.root / "fail-check").touch()
        self.run_shell('shadowsocksApply install "$SS_TEST_ROOT/candidate.json"', success=False)
        self.assertEqual((self.managed / "config.json").read_bytes(), config)
        self.assertTrue((self.root / "active").exists())

    def test_occupied_port_and_concurrent_operation(self):
        (self.root / "occupied").touch()
        self.run_shell('''
shadowsocksGenerateConfig 8388 aes-256-gcm pass >"$SS_TEST_ROOT/candidate.json" &&
shadowsocksApply install "$SS_TEST_ROOT/candidate.json"
''', success=False)
        self.assertFalse((self.managed / "config.json").exists())
        (self.managed / ".lock").mkdir()
        self.run_shell("shadowsocksApply remove", success=False)

    def test_ipv6_share_link_and_clash_node(self):
        self.install()
        output = self.run_shell("shadowsocksShow 2001:db8::1").stdout
        link = next(line for line in output.splitlines() if line.startswith("ss://"))
        self.assertIn("@[2001:db8::1]:8388", link)
        userinfo = link[5:].split("@", 1)[0]
        self.assertEqual(base64.urlsafe_b64decode(userinfo + "=" * (-len(userinfo) % 4)).decode(), "aes-256-gcm:test-password")
        node = json.loads(output[output.index("{"):])
        self.assertEqual(node["server"], "2001:db8::1")
        self.assertTrue(node["udp"])

    def test_ss2022_share_key_is_url_encoded(self):
        key = base64.b64encode(bytes([255] * 16)).decode()
        self.run_shell(f'''shadowsocksGenerateConfig 8388 2022-blake3-aes-128-gcm '{key}' >"$SS_TEST_ROOT/agent/shadowsocks/config.json"''')
        result = self.run_shell("shadowsocksShow example.com")
        self.assertIn("ss://2022-blake3-aes-128-gcm:%2F", result.stdout)
        self.assertIn("%3D%3D@example.com:8388", result.stdout)


class EnglishShadowsocksTests(ShadowsocksTests):
    script = "shell/install_en.sh"


if __name__ == "__main__":
    unittest.main()
