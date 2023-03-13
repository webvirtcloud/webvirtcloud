desc = "Debian based eth2 interfaces file template"
data = """
# The third network interface
auto eth2
iface eth2 inet static
    address {{ ipv4private.address }}
    netmask {{ ipv4private.netmask }}"""
