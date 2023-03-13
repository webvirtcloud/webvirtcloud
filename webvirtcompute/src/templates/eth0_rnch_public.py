desc = "RancherOS based eth0 interface file template for public cloud"
data = """#cloud-config

rancher:
  network:
    interfaces:
      eth0:
        addresses:
        - {{ ipv4public.address }}/{{ ipv4public.prefix }}
        - {{ ipv4compute.address }}/{{ ipv4compute.prefix }}
        {% if ipv6public %}
        - {{ ipv6public.address }}/{{ ipv6public.prefix }}
        {% endif %}
        gateway: {{ ipv4public.gateway }}
        {% if ipv6public %}
        gateway_ipv6: {{ ipv6public.gateway }}
        {% endif %}
        dns:
          nameservers:
          - {{ ipv4public.dns1 }}
          - {{ ipv4public.dns1 }}
          {% if ipv6public %}
          - {{ ipv6public.dns1 }}
          - {{ ipv6public.dns2 }}
          {% endif %}"""
