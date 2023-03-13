desc = "RancherOS based eth0 interface file template for private cloud"
data = """#cloud-config

rancher:
  network:
    interfaces:
      eth0:
        addresses:
        - {{ ipv4public.address }}/{{ ipv4public.prefix }}
        gateway: {{ ipv4public.gateway }}
        dns:
          nameservers:
          - {{ ipv4public.dns1 }}
          - {{ ipv4public.dns2 }}"""
