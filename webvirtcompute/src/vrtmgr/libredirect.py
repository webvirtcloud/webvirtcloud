import os
import time
import socket
from subprocess import call, STDOUT, DEVNULL
from firewall.client import FirewallClient
from settings import BRIDGE_EXT, FIREWALL_CHAIN_PREFIX
from settings import FIREWALLD_STATE_TIMEOUT, FIREWALLD_STATE_FILE

import gi
gi.require_version("NM", "1.0")
from gi.repository import NM


class FwRedirect(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.fw = FirewallClient()
        self.config = self.fw.config()
        self.fw_direct = self.config.direct()
        self.prio = 0
        self.ipv4 = "ipv4"
        self.table = "nat"
        self.jmp = "DNAT"
        self.iptable = f"iptables -t {self.table}"
        self.chain = f"PREROUTING{FIREWALL_CHAIN_PREFIX}"
        self.args = ["-d", self.src, "-j", self.jmp, "--to-destination", self.dst]

    def set_state(self):
        f = open(FIREWALLD_STATE_FILE, "w")
        f.write("1")
        f.close()

    def unset_state(self):
        f = open(FIREWALLD_STATE_FILE, "w")
        f.write("0")
        f.close()

    def read_state(self):
        if os.path.isfile(FIREWALLD_STATE_FILE):
            f = open(FIREWALLD_STATE_FILE, "r")
            f_data = f.read()
            f.close()
            if f_data:
                state = eval(f_data)
            else:
                self.unset_state()
                state = False
            return state
        else:
            return False

    def is_locked(self):
        if self.read_state():
            seconds = 0
            while self.read_state():
                seconds += 1
                time.sleep(1)
                if seconds >= FIREWALLD_STATE_TIMEOUT:
                    return True
        return False

    def save(self):
        self.fw_direct.update(self.fw_direct.getSettings())
        self.unset_state()

    def reload(self):
        self.fw.reload()

    def query_rule(self):
        cmd = f"{self.iptable} -C {self.chain} -d {self.src} -j {self.jmp} --to-destination {self.dst}"
        run_cmd = call(cmd.split(), stdout=DEVNULL, stderr=STDOUT)
        if run_cmd == 1:
            return False
        return True

    def check_rule_in_xml(self):
        res = self.fw_direct.queryRule(self.ipv4, self.table, self.chain, self.prio, self.args)
        return res

    def add_rule(self):
        if not self.query_rule():
            cmd = f"{self.iptable} -A {self.chain} -d {self.src} -j {self.jmp} --to-destination {self.dst}"
            run_cmd = call(cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_cmd == 0:
                if not self.check_rule_in_xml():
                    self.fw_direct.addRule(self.ipv4, self.table, self.chain, self.prio, self.args)
                    self.save()

    def remove_rule(self):
        if self.query_rule():
            cmd = f"{self.iptable} -D {self.chain} -d {self.src} -j {self.jmp} --to-destination {self.dst}"
            run_cmd = call(cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_cmd == 0:
                if self.check_rule_in_xml():
                    self.fw_direct.removeRule(self.ipv4, self.table, self.chain, self.prio, self.args)
                    self.save()


class NetManager(object):
    def __init__(self, src_ip):
        self.dev = BRIDGE_EXT
        self.src = src_ip
        self.nmc = NM.Client.new(None)

    def get_ip_addresses(self):
        ip_addrs = []
        dev = self.nmc.get_device_by_iface(self.dev)
        ips_cfg = dev.get_ip4_config()
        for addr in ips_cfg.get_addresses():
            ip_addrs.append(addr.get_address())
        return ip_addrs

    def add_address(self, prefix=32):
        ip_addr = NM.IPAddress.new(socket.AF_INET, self.src, int(prefix))
        dev = self.nmc.get_device_by_iface(self.dev)
        dev_conn = dev.get_active_connection()
        conn = self.nmc.get_connection_by_id(dev_conn.get_id())
        ipcfg = conn.get_setting_ip4_config()
        ipcfg.add_address(ip_addr)
        conn.commit_changes(True)

    def remove_address(self, prefix=32):
        ip_addr = NM.IPAddress.new(socket.AF_INET, self.src, int(prefix))
        dev = self.nmc.get_device_by_iface(self.dev)
        dev_conn = dev.get_active_connection()
        conn = self.nmc.get_connection_by_id(dev_conn.get_id())
        ipcfg = conn.get_setting_ip4_config()
        ipcfg.remove_address_by_value(ip_addr)
        conn.commit_changes(True)
