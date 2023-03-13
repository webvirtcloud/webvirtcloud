desc = "RedHat based eth0 interface file template for public cloud"
data = """DEVICE=eth0
TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=none
NM_CONTROLLED=yes
IPADDR1={{ ipv4public.address }}
PREFIX1={{ ipv4public.prefix }}
GATEWAY1={{ ipv4public.gateway }}
IPADDR2={{ ipv4compute.address }}
PREFIX2={{ ipv4compute.prefix }}
DNS1={{ ipv4public.dns1 }}
DNS2={{ ipv4public.dns2 }}
{% if ipv6public %}
IPV6INIT=yes
IPV6_AUTOCONF=no
IPV6ADDR={{ ipv6public.address }}/{{ ipv6public.prefix }}
IPV6_DEFAULTGW={{ ipv6public.gateway }}
DNS1={{ ipv6public.dns1 }}
DNS2={{ ipv6public.dns2 }}
{% endif %}"""
