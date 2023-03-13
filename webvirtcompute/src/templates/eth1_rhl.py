desc = "RedHat based eth1 interface file template"
data = """DEVICE=eth1
TYPE=Ethernet
ONBOOT=yes
DEFROUTE=no
BOOTPROTO=none
NM_CONTROLLED=yes
IPADDR={{ ipv4private.address }}
NETMASK={{ ipv4private.netmask }}"""
