from subprocess import call, STDOUT, DEVNULL
from settings import BRIDGE_EXT, FIREWALLD_STATE_TIMEOUT
from .libguestfs import GuestFSUtil
from .excpetions import IPRedirectError
from .libredirect import FwRedirect, NetManager


class FixedIP(object):
    def __init__(self, fixed_ip):
        self.fixed_ip = fixed_ip

    def attach_floating_ip(self, floating_ip, floating_prefix, floating_gw):
        err_msg = None
        try:
            nmc = NetManager(floating_ip)
            fwd = FwRedirect(floating_ip, self.fixed_ip)
            dev = BRIDGE_EXT
            self.add_redirect(fwd, floating_ip, floating_prefix, floating_gw, nmc, dev)
        except IPRedirectError as err:
            err_msg = err

        return err_msg

    def detach_floating_ip(self, floating_ip, floating_prefix):
        err_msg = None
        dev = BRIDGE_EXT
        nmc = NetManager(floating_ip)
        fwd = FwRedirect(floating_ip, self.fixed_ip)
        try:
            self.remove_redirect(fwd, floating_ip, floating_prefix, nmc, dev)
        except IPRedirectError as err:
            err_msg = err

        return err_msg

    def change_fixed_ip(self, image_path, distro):
        err_msg = None
        try:
            # Load GuestFS
            gstfish = GuestFSUtil(image_path, distro)
            gstfish.mount_root()
            gstfish.change_ipv4anch(self.fixed_ip)
            gstfish.close()
        except RuntimeError as err:
            err_msg = err

        return err_msg

    def add_addr(self, float_addr, nmc, dev, prefix=32):
        if float_addr not in nmc.get_ip_addresses():
            ip_cmd = f"ip addr add {float_addr}/{prefix} dev {dev}"
            run_ip_cmd = call(ip_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_ip_cmd == 0:
                nmc.add_address(prefix=prefix)
                return True
        return False

    def del_addr(self, nmc, float_addr, dev, prefix=32):
        if float_addr in nmc.get_ip_addresses():
            ip_cmd = f"ip addr del {float_addr}/{prefix} dev {dev}"
            run_ip_cmd = call(ip_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_ip_cmd == 0:
                nmc.remove_address(prefix)
                return True
        return False

    def check_rule(self, fwd):
        return fwd.query_rule()

    def add_rule(self, fwd):
        if not self.check_rule(fwd):
            fwd.add_rule()

    def del_rule(self, fwd):
        if self.check_rule(fwd):
            fwd.remove_rule()

    def clear_arp(self, float_addr, float_gw, dev):
        arp_cmd = f"arping -c 3 -s {float_addr} -I {dev} -U {float_gw}"
        run_arp_cmd = call(arp_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
        if run_arp_cmd == 0:
            return True

    def add_redirect(self, fwd, float_addr, float_pref, float_gw, nmc, dev):
        if self.add_addr(float_addr, nmc, dev, prefix=float_pref):
            if not fwd.is_locked():
                fwd.set_state()
                self.add_rule(fwd)
                self.clear_arp(float_addr, float_gw, dev)
            else:
                self.del_addr(nmc, float_addr, dev, prefix=float_pref)
                raise IPRedirectError(f"Firewall closed connection by timeout {FIREWALLD_STATE_TIMEOUT}sec.")
        else:
            raise IPRedirectError("Error adding IP address to the network device.")

    def remove_redirect(self, fwd, float_addr, float_pref, nmc, dev):
        if self.del_addr(nmc, float_addr, dev, prefix=float_pref):
            if not fwd.is_locked():
                fwd.set_state()
                self.del_rule(fwd)
            else:
                self.add_addr(float_addr, nmc, dev, prefix=float_pref)
                raise IPRedirectError(f"Firewall closed connection by timeout {FIREWALLD_STATE_TIMEOUT}sec.")
        else:
            raise IPRedirectError("Error deleting IP address from the network device.")
