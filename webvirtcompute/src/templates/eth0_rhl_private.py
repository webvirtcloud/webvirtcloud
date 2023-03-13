desc = "RedHat based eth0 interface file template for private cloud"
data = """DEVICE=eth0
TYPE=Ethernet
ONBOOT=yes
IPV6INIT=no
BOOTPROTO=none
NM_CONTROLLED=yes
IPADDR1={{ ipv4public.address }}
PREFIX1={{ ipv4public.prefix }}
GATEWAY={{ ipv4public.gateway }}
DNS1={{ ipv4public.dns1 }}
DNS2={{ ipv4public.dns2 }}"""
