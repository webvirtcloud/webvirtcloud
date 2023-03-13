desc = "RancherOS based eth1 interfaces file template"
data = """
      eth1:
        address: {{ ipv4private.address }}/{{ ipv4private.prefix }}"""
