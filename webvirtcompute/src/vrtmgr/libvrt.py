import os
import time
import base64
import string
import libvirt
import binascii
import datetime
from uuid import UUID
from xml.etree import ElementTree
from ipaddress import IPv4Interface

import settings
from . import util


DISPLAY = "vnc"
VENDOR = "WebVirtCloud"
PRODUCT = "Virtance"
VERSION = "20230101"
MANUFACTURER = "WebVirtCloud"


class wvmConnect(object):
    def __init__(self):
        self.wvm = libvirt.open("qemu:///system")

    def get_cap_xml(self):
        return self.wvm.getCapabilities()

    def is_kvm_supported(self):
        return util.is_kvm_available(self.get_cap_xml())

    def get_domain_type(self):
        return "kvm" if self.is_kvm_supported() else "qemu"

    def get_host_info(self):
        nodeinfo = self.wvm.getInfo()
        processor = util.get_xml_data(self.wvm.getSysinfo(0), "processor/entry[6]")
        return {
            "hostname": self.wvm.getHostname(),
            "arch": nodeinfo[0],
            "memory": nodeinfo[1] * (1024**2),
            "cpus": nodeinfo[2],
            "processor": processor if processor else "Unknown",
            "connection": self.wvm.getURI(),
        }

    def get_host_type(self):
        return util.get_xml_data(self.get_cap_xml(), "guest/arch/domain", "type")

    def get_host_mem_usage(self):
        host_memory = self.wvm.getInfo()[1] * (1024**2)
        free_memory = self.wvm.getMemoryStats(-1, 0)
        if isinstance(free_memory, dict):
            memory = list(free_memory.values())
            free = (memory[1] + memory[2] + memory[3]) * 1024
            memory_usage = host_memory - free
            return {"usage": memory_usage}
        return {"usage": 0}

    def get_host_cpu_usage(self):
        prev_idle = prev_total = diff_usage = 0
        cpu = self.wvm.getCPUStats(-1, 0)
        if isinstance(cpu, dict):
            for num in range(2):
                idle = self.wvm.getCPUStats(-1, 0)["idle"]
                total = sum(self.wvm.getCPUStats(-1, 0).values())
                diff_idle = idle - prev_idle
                diff_total = total - prev_total
                diff_usage = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10
                prev_total = total
                prev_idle = idle
                if num == 0:
                    time.sleep(1)
                if diff_usage < 0:
                    diff_usage = 0
        return {"usage": round(diff_usage)}

    def get_storages(self):
        storages = []
        for pool in self.wvm.listStoragePools():
            storages.append(pool)
        for pool in self.wvm.listDefinedStoragePools():
            storages.append(pool)
        return storages

    def get_storage(self, name):
        return self.wvm.storagePoolLookupByName(name)

    def get_storage_usage(self, name):
        pool = self.get_storage(name)
        pool.refresh()
        if pool.isActive():
            size = pool.info()[1]
            free = pool.info()[3]
            used = size - free
            percent = (used * 100) / size
            return {"size": size, "used": used, "percent": percent}
        return {"size": 0, "used": 0, "percent": 0}

    def get_networks(self):
        virtnet = []
        for net in self.wvm.listNetworks():
            virtnet.append(net)
        for net in self.wvm.listDefinedNetworks():
            virtnet.append(net)
        return virtnet

    def refresh_storages(self):
        for pool in self.wvm.listStoragePools():
            stg = self.wvm.storagePoolLookupByName(pool)
            stg.refresh()

    def get_ifaces(self):
        interface = []
        for inface in self.wvm.listInterfaces():
            interface.append(inface)
        for inface in self.wvm.listDefinedInterfaces():
            interface.append(inface)
        return interface

    def get_iface(self, name):
        return self.wvm.interfaceLookupByName(name)

    def get_secrets(self):
        return self.wvm.listSecrets()

    def get_secret(self, uuid):
        return self.wvm.secretLookupByUUIDString(uuid)

    def get_nwfilters(self):
        return self.wvm.listNWFilters()

    def get_nwfilter(self, name):
        return self.wvm.nwfilterLookupByName(name)

    def get_volume_by_path(self, path):
        return self.wvm.storageVolLookupByPath(path)

    def get_network(self, net):
        return self.wvm.networkLookupByName(net)

    def get_instance(self, name):
        return self.wvm.lookupByName(name)

    def get_instance_by_uuid(self, uuid):
        return self.wvm.lookupByUUIDString(uuid)

    def get_instance_status(self, name):
        dom = self.wvm.lookupByName(name)
        return dom.info()[0]

    def get_instances(self):
        instances = []
        for inst_id in self.wvm.listDomainsID():
            dom = self.wvm.lookupByID(int(inst_id))
            instances.append(dom.name())
        for name in self.wvm.listDefinedDomains():
            instances.append(name)
        return instances

    def get_snapshots(self):
        instance = []
        for snap_id in self.wvm.listDomainsID():
            dom = self.wvm.lookupByID(int(snap_id))
            if dom.snapshotNum(0) != 0:
                instance.append(dom.name())
        for name in self.wvm.listDefinedDomains():
            dom = self.wvm.lookupByName(name)
            if dom.snapshotNum(0) != 0:
                instance.append(dom.name())
        return instance

    def get_net_device(self):
        netdevice = []
        for dev in self.wvm.listAllDevices(0):
            xml = dev.XMLDesc(0)
            if util.get_xml_data(xml, "capability", "type") == "net":
                netdevice.append(util.get_xml_data(xml, "capability/interface"))
        return netdevice

    def get_host_instances(self):
        vname = []
        for name in self.get_instances():
            dom = self.get_instance(name)
            mem = util.get_xml_data(dom.XMLDesc(0), "currentMemory")
            mem = round(int(mem) / 1024)
            cur_vcpu = util.get_xml_data(dom.XMLDesc(0), "vcpu", "current")
            if cur_vcpu:
                vcpu = cur_vcpu
            else:
                vcpu = util.get_xml_data(dom.XMLDesc(0), "vcpu")
            vname.append(
                {"name": dom.name(), "status": dom.info()[0], "uuid": dom.UUIDString(), "vcpu": vcpu, "memory": mem}
            )
        return vname

    def close(self):
        self.wvm.close()


class wvmStorages(wvmConnect):
    def get_storages_info(self):
        storages = []
        stg_volumes = 0
        for pool in self.get_storages():
            stg = self.get_storage(pool)
            stg_active = bool(stg.isActive())
            stg_type = util.get_xml_data(stg.XMLDesc(0), element="type")
            if stg_active:
                stg_volumes = len(stg.listVolumes())                
            stg_size = stg.info()[1]
            storages.append(
                {
                    "name": pool,
                    "type": stg_type,
                    "size": stg_size,
                    "active": stg_active,
                    "volumes": stg_volumes,
                }
            )
        return storages

    def define_storage(self, xml, flag):
        self.wvm.storagePoolDefineXML(xml, flag)

    def create_storage(self, stg_type, name, source, target):
        xml = f"""
                <pool type='{stg_type}'>
                <name>{name}</name>"""
        if stg_type == "logical":
            xml += f"""
                  <source>
                    <device path='{source}'/>
                    <name>{name}</name>
                    <format type='lvm2'/>
                  </source>"""
        if stg_type == "logical":
            target = "/dev/" + name
        xml += f"""
                  <target>
                       <path>{target}</path>
                  </target>
                </pool>"""
        self.define_storage(xml, 0)
        stg = self.get_storage(name)
        if stg_type == "logical":
            stg.build(0)
        stg.create(0)
        stg.setAutostart(1)

    def create_storage_ceph(self, stg_type, name, pool, host1, host2, host3, user, secret):
        xml = f"""
                <pool type='{stg_type}'>
                <name>{name}</name>
                <source>
                    <name>{pool}</name>
                    <host name='{host1}' port='6789'/>"""
        if host2:
            xml += f"""<host name='{host2}' port='6789'/>"""
        if host3:
            xml += f"""<host name='{host3}' port='6789'/>"""

        xml += """<auth username='%s' type='ceph'>
                        <secret uuid='%s'/>
                    </auth>
                </source>
                </pool>""" % (
            user,
            secret,
        )
        self.define_storage(xml, 0)
        stg = self.get_storage(name)
        stg.create(0)
        stg.setAutostart(1)

    def create_storage_netfs(self, stg_type, name, netfs_host, source, source_format, target):
        xml = f"""
                <pool type='{stg_type}'>
                <name>{name}</name>
                <source>
                    <host name='{netfs_host}'/>
                    <dir path='{source}'/>
                    <format type='{source_format}'/>
                </source>
                <target>
                    <path>{target}</path>
                </target>
                </pool>"""
        self.define_storage(xml, 0)
        stg = self.get_storage(name)
        stg.create(0)
        stg.setAutostart(1)


class wvmStorage(wvmConnect):
    def __init__(self, pool):
        wvmConnect.__init__(self)
        self.pool = self.get_storage(pool)

    def get_name(self):
        return self.pool.name()

    def get_active(self):
        return bool(self.pool.isActive())

    def get_status(self):
        status = ["Not running", "Initializing pool, not available", "Running normally", "Running degraded"]
        try:
            return status[self.pool.info()[0]]
        except ValueError:
            return "Unknown"

    def get_total_size(self):
        return self.pool.info()[1]

    def get_used_size(self):
        return self.pool.info()[3]

    def get_free_size(self):
        return self.pool.info()[3]

    def XMLDesc(self, flags):
        return self.pool.XMLDesc(flags)

    def createXML(self, xml, flags):
        self.pool.createXML(xml, flags)

    def createXMLFrom(self, xml, vol, flags):
        self.pool.createXMLFrom(xml, vol, flags)

    def define(self, xml):
        return self.wvm.storagePoolDefineXML(xml, 0)

    def is_active(self):
        return bool(self.pool.isActive())

    def get_uuid(self):
        return self.pool.UUIDString()

    def start(self):
        self.pool.create(0)

    def stop(self):
        self.pool.destroy()

    def delete(self):
        self.pool.undefine()

    def refresh(self):
        self.pool.refresh(0)

    def get_autostart(self):
        return bool(self.pool.autostart())

    def set_autostart(self, value):
        self.pool.setAutostart(value)

    def get_type(self):
        return util.get_xml_data(self.XMLDesc(0), element="type")

    def get_target_path(self):
        return util.get_xml_data(self.XMLDesc(0), "target/path")

    def get_allocation(self):
        return int(util.get_xml_data(self.XMLDesc(0), "allocation"))

    def get_available(self):
        return int(util.get_xml_data(self.XMLDesc(0), "available"))

    def get_capacity(self):
        return int(util.get_xml_data(self.XMLDesc(0), "capacity"))

    def get_pretty_allocation(self):
        return util.pretty_bytes(self.get_allocation())

    def get_pretty_available(self):
        return util.pretty_bytes(self.get_available())

    def get_pretty_capacity(self):
        return util.pretty_bytes(self.get_capacity())

    def get_volumes(self):
        try:
            self.refresh()
        except Exception:
            pass
        if self.get_active() is True:
            return self.pool.listVolumes()
        return []

    def get_volume(self, name):
        return self.pool.storageVolLookupByName(name)

    def get_volume_size(self, name):
        vol = self.get_volume(name)
        return vol.info()[1]

    def _vol_XMLDesc(self, name):
        vol = self.get_volume(name)
        return vol.XMLDesc(0)

    def del_volume(self, name):
        vol = self.pool.storageVolLookupByName(name)
        vol.delete(0)

    def get_volume_type(self, name):
        return util.get_xml_data(self._vol_XMLDesc(name), "target/format", "type")

    def get_volume_info(self, name):
        return {"name": name, "size": self.get_volume_size(name), "type": self.get_volume_type(name)}

    def get_volumes_info(self):
        try:
            self.refresh()
        except Exception:
            pass
        vols = self.get_volumes()
        vol_list = []

        for volname in vols:
            vol_list.append(
                {"name": volname, "size": self.get_volume_size(volname), "type": self.get_volume_type(volname)}
            )
        return vol_list

    def resize_volume(self, name, size):
        vol = self.get_volume(name)
        vol.resize(size)

    def create_volume(self, name, size, fmt="qcow2", metadata=False):
        storage_type = self.get_type()
        alloc = size
        if fmt == "unknown":
            fmt = "raw"
        if storage_type == "dir":
            name += ".img"
            alloc = 0
        xml = f"""
            <volume>
                <name>{name}</name>
                <capacity>{size}</capacity>
                <allocation>{alloc}</allocation>
                <target>
                    <format type='{fmt}'/>
                </target>
            </volume>"""
        self.createXML(xml, metadata)

    def clone_volume(self, name, clone, fmt=None, metadata=False):
        storage_type = self.get_type()
        if storage_type == "dir":
            clone += ".img"
        vol = self.get_volume(name)
        if fmt is None:
            fmt = self.get_volume_type(name)
        xml = f"""
            <volume>
                <name>{clone}</name>
                <capacity>0</capacity>
                <allocation>0</allocation>
                <target>
                    <format type='{fmt}'/>
                </target>
            </volume>"""
        self.createXMLFrom(xml, vol, metadata)


class wvmNetworks(wvmConnect):
    def get_networks_info(self):
        networks = []
        for network in self.get_networks():
            net = self.get_network(network)
            net_active = bool(net.isActive())
            net_bridge = net.bridgeName()
            net_forwd = util.get_xml_data(net.XMLDesc(0), "forward", "mode")
            networks.append({"name": network, "active": net_active, "device": net_bridge, "forward": net_forwd})
        return networks

    def define_network(self, xml):
        self.wvm.networkDefineXML(xml)

    def create_network(self, name, forward, gateway, mask, dhcp, bridge, openvswitch, fixed=False):
        xml = f"""
            <network>
                <name>{name}</name>"""
        if forward in ["nat", "route", "bridge"]:
            xml += f"""<forward mode='{forward}'/>"""
        xml += """<bridge """
        if forward in ["nat", "route", "none"]:
            xml += """stp='on' delay='0'"""
        if forward == "bridge":
            xml += f"""name='{bridge}'"""
        xml += """/>"""
        if openvswitch is True:
            xml += """<virtualport type='openvswitch'/>"""
        if forward != "bridge":
            xml += f"""<ip address='{gateway}' netmask='{mask}'>"""
            if dhcp:
                xml += f"""<dhcp>
                            <range start='{dhcp[0]}' end='{dhcp[1]}' />"""
                if fixed:
                    fist_oct = int(dhcp[0].strip().split(".")[3])
                    last_oct = int(dhcp[1].strip().split(".")[3])
                    for ip in range(fist_oct, last_oct + 1):
                        xml += f"""<host mac='{util.randomMAC()}' ip='{gateway[:-2]}.{ip}' />"""
                xml += """</dhcp>"""

            xml += """</ip>"""
        xml += """</network>"""
        self.define_network(xml)
        net = self.get_network(name)
        net.create()
        net.setAutostart(1)


class wvmNetwork(wvmConnect):
    def __init__(self, net):
        wvmConnect.__init__(self)
        self.net = self.get_network(net)

    def get_name(self):
        return self.net.name()

    def XMLDesc(self, flags):
        return self.net.XMLDesc(flags)

    def define(self, xml):
        self.wvm.networkDefineXML(xml)

    def get_autostart(self):
        return bool(self.net.autostart())

    def set_autostart(self, value):
        self.net.setAutostart(value)

    def get_active(self):
        return bool(self.net.isActive())

    def get_uuid(self):
        return self.net.UUIDString()

    def get_bridge_device(self):
        try:
            return self.net.bridgeName()
        except Exception:
            return None

    def start(self):
        self.net.create()

    def stop(self):
        self.net.destroy()

    def delete(self):
        self.net.undefine()

    def get_ipv4_network(self):
        xml = self.XMLDesc(0)
        if not util.get_xml_data(xml, "ip"):
            return None

        ip = util.get_xml_data(xml, "ip", "address")
        prefix = util.get_xml_data(xml, "ip", "prefix")
        netmask = util.get_xml_data(xml, "ip", "netmask")

        if netmask:
            ipv4_iface = IPv4Interface(f"{ip}/{netmask}")

        if prefix:
            ipv4_iface = IPv4Interface(f"{ip}/{prefix}")

        return f"{ipv4_iface.ip}/{str(ipv4_iface.netmask)}"

    def get_ipv4_forward(self):
        xml = self.XMLDesc(0)
        fw = util.get_xml_data(xml, "forward", "mode")
        forwardDev = util.get_xml_data(xml, "forward", "dev")
        return [fw, forwardDev]

    def get_ipv4_dhcp_range(self):
        xml = self.XMLDesc(0)
        dhcpstart = util.get_xml_data(xml, "ip/dhcp/range[1]", "start")
        dhcpend = util.get_xml_data(xml, "ip/dhcp/range[1]", "end")
        if not dhcpstart and not dhcpend:
            return None
        return [dhcpstart, dhcpend]

    def get_ipv4_dhcp_range_start(self):
        dhcp = self.get_ipv4_dhcp_range()
        if not dhcp:
            return None
        return dhcp[0]

    def get_ipv4_dhcp_range_end(self):
        dhcp = self.get_ipv4_dhcp_range()
        if not dhcp:
            return None
        return dhcp[1]

    def can_pxe(self):
        xml = self.XMLDesc(0)
        forward = self.get_ipv4_forward()[0]
        if forward and forward != "nat":
            return True
        return bool(util.get_xml_data(xml, "ip/dhcp/bootp", "file"))

    def get_mac_ipaddr(self):
        fixed_mac = []
        xml = self.XMLDesc(0)
        tree = ElementTree.fromstring(xml)
        dhcp_list = tree.findall("ip/dhcp/host")
        for i in dhcp_list:
            fixed_mac.append({"host": i.get("ip"), "mac": i.get("mac")})
        return fixed_mac


class wvmSecrets(wvmConnect):
    def create_secret(self, ephemeral, private, secret_type, data):
        xml = f"""<secret ephemeral='{ephemeral}' private='{private}'>
                    <usage type='{secret_type}'>"""
        if secret_type == "ceph":
            xml += f"""<name>{data}</name>"""
        if secret_type == "volume":
            xml += f"""<volume>{data}</volume>"""
        if secret_type == "iscsi":
            xml += f"""<target>{data}</target>"""
        xml += """</usage>
                 </secret>"""
        self.wvm.secretDefineXML(xml)

    def get_secret_value(self, uuid):
        secret = self.get_secret(uuid)
        try:
            value = secret.value()
        except libvirt.libvirtError:
            return None
        return base64.b64encode(value)

    def set_secret_value(self, uuid, value):
        secret = self.get_secret(uuid)
        try:
            value = base64.b64decode(value)
            secret.setValue(value)
        except (TypeError, binascii.Error) as err:
            raise libvirt.libvirtError(err)

    def delete_secret(self, uuid):
        secret = self.get_secret(uuid)
        secret.undefine()


class wvmNWfilter(wvmConnect):
    def create_nwfilter(self, xml):
        self.wvm.nwfilterDefineXML(xml)

    def get_nwfilter_xml(self, name):
        nw = self.get_nwfilter(name)
        return nw.XMLDesc()

    def delete_nwfilter(self, name):
        nw = self.get_nwfilter(name)
        nw.undefine()


class wvmCreate(wvmConnect):
    def get_storages_images(self):
        images = []
        storages = self.get_storages()
        for storage in storages:
            stg = self.get_storage(storage)
            try:
                stg.refresh(0)
            except libvirt.libvirtError:
                pass
            for img in stg.listVolumes():
                if img.endswith(".iso"):
                    pass
                else:
                    images.append(img)
        return images

    def get_os_type(self):
        return util.get_xml_data(self.get_cap_xml(), "guest/os_type")

    def get_host_arch(self):
        return util.get_xml_data(self.get_cap_xml(), "host/cpu/arch")

    def create_volume(self, storage, name, size, volume_format="qcow2", metadata=False):
        stg = self.get_storage(storage)
        storage_type = util.get_xml_data(stg.XMLDesc(0), element="type")
        if storage_type == "dir":
            name = f"{str(name)}.img"
            alloc = 0
        else:
            alloc = size
            metadata = False
        xml = f"""
                <volume>
                    <name>{name}</name>
                    <capacity>{size}</capacity>
                    <allocation>{alloc}</allocation>
                    <target>
                        <format type='{volume_format}'/>
                    </target>
                </volume>"""
        stg.createXML(xml, metadata)
        try:
            stg.refresh(0)
        finally:
            vol = stg.storageVolLookupByName(name)
            return vol.path()

    def get_volume_type(self, path):
        vol = self.get_volume_by_path(path)
        vol_type = util.get_xml_data(vol.XMLDesc(0), "target/format", "type")
        if vol_type == "unknown":
            return "raw"
        if vol_type:
            return vol_type
        else:
            return "raw"

    def get_volume_path(self, volume):
        storages = self.get_storages()
        for storage in storages:
            stg = self.get_storage(storage)
            if stg.info()[0] != 0:
                stg.refresh(0)
                for img in stg.listVolumes():
                    if img == volume:
                        vol = stg.storageVolLookupByName(img)
                        return vol.path()

    def get_storage_by_vol_path(self, vol_path):
        vol = self.get_volume_by_path(vol_path)
        return vol.storagePoolLookupByVolume()

    def clone_from_template(self, clone, template, metadata=False):
        vol = self.get_volume_by_path(template)
        stg = vol.storagePoolLookupByVolume()
        storage_type = util.get_xml_data(stg.XMLDesc(0), element="type")
        vol_type = util.get_xml_data(vol.XMLDesc(0), "target/format", "type")
        if storage_type == "dir":
            clone += ".img"
        else:
            metadata = False
        xml = f"""
                <volume>
                    <name>{clone}</name>
                    <capacity>0</capacity>
                    <allocation>0</allocation>
                    <target>
                        <format type='{vol_type}'/>
                    </target>
                </volume>"""
        stg.createXMLFrom(xml, vol, metadata)
        clone_vol = stg.storageVolLookupByName(clone)
        return clone_vol.path()

    def defineXML(self, xml):
        self.wvm.defineXML(xml)

    def delete_volume(self, path):
        vol = self.get_volume_by_path(path)
        vol.delete()

    def get_rbd_storage_data(self, stg):
        hosts = []
        xml = stg.XMLDesc(0)
        host_count = xml.find("host")
        username = util.get_xml_data(xml, "source/auth", "username")
        uuid = util.get_xml_data(xml, "source/auth/secret", "uuid")
        for i in range(1, host_count + 1):
            host = util.get_xml_data(xml, f"source/host[{i}]", "name")
            if host:
                hosts.append(host)
        return username, uuid, hosts

    def create_xml(
        self, name, vcpu, memory, images, network, uuid=None, autostart=True, nwfilter=True, display=DISPLAY
    ):
        xml = f"""<domain type='{self.get_domain_type()}'>
                    <name>{name}</name>
                """
        if uuid:
            xml += f"""<uuid>{str(UUID(uuid))}</uuid>"""

        xml += f"""<description>None</description>
                  <memory unit='KiB'>{int(memory // 1024)}</memory>
                  <vcpu>{vcpu}</vcpu>
                """

        if self.is_kvm_supported():
            xml += """<cpu mode='host-passthrough'/>"""

        xml += f"""<sysinfo type='smbios'>
                    <bios>
                      <entry name='vendor'>{VENDOR}</entry>
                      <entry name='version'>{VERSION}</entry>
                      <entry name='date'>11/25/2022</entry>
                    </bios>
                    <system>
                     <entry name='manufacturer'>{MANUFACTURER}</entry>
                      <entry name='product'>{PRODUCT}</entry>
                      <entry name='version'>{VERSION}</entry>
                      <entry name='serial'>{name.split('-')[1]}</entry>
                      <entry name='family'>{MANUFACTURER}_{PRODUCT}</entry>
                    </system>
                   </sysinfo>
                """

        xml += f"""<os>
                    <type arch='{self.get_host_arch()}'>{self.get_os_type()}</type>
                    <boot dev='cdrom'/>
                    <boot dev='hd'/>
                    <smbios mode='sysinfo'/>
                   </os>
                """

        xml += """<features>
                   <acpi/><apic/><pae/>
                  </features>
                  <clock offset="utc"/>
                  <on_poweroff>destroy</on_poweroff>
                  <on_reboot>restart</on_reboot>
                  <on_crash>restart</on_crash>
                  <devices>
                """

        disk_letters = list(string.ascii_lowercase)
        for image in images:
            stg = self.get_storage(settings.STORAGE_IMAGE_POOL)
            stg_xml = stg.XMLDesc(0)
            stg_type = util.get_xml_data(stg_xml, element="type")

            if stg_type == "rbd":
                ceph_user, secrt_uuid, ceph_host = self.get_rbd_storage_data(stg)

                xml += f"""<disk type='network' device='disk'>
                            <driver name='qemu' type='raw' cache='writeback'/>
                            <auth username='{ceph_user}'>
                             <secret type='ceph' uuid='{secrt_uuid}'/>
                            </auth>
                            <source protocol='rbd' name='{image.get('name')}'>
                             <host name='{ceph_host}' port='6789'/>
                            </source>
                           </disk>
                        """
            else:
                stg_path = util.get_xml_data(stg_xml, path="target/path")
                xml += f"""<disk type='file' device='disk'>
                            <driver name='qemu' type='raw'/>
                            <source file='{stg_path}/{image.get('name')}.img'/>
                            <target dev='vd{disk_letters.pop(0)}' bus='virtio'/>
                           </disk>
                        """

        xml += """<disk type='file' device='cdrom'>
                   <driver name='qemu' type='raw'/>
                   <source file=''/>
                   <target dev='hda' bus='ide'/>
                   <readonly/>
                  </disk>
                """

        # Create public pool device with IPv4 and IPv6 and internal IPv4
        if network.get("v4", {}).get("public"):
            xml += """<interface type='network'>"""

            if network.get("v4", {}).get("public", {}).get("mac"):
                xml += f"""<mac address='{network.get('v4', {}).get('public', {}).get('mac')}'/>"""

            if network.get("v4", {}).get("public", {}).get("pool"):
                xml += f"""<source network='{network.get('v4', {}).get('public', {}).get('pool')}'/>"""
            else:
                xml += f"""<source network='{settings.NETWORK_PUBLIC_POOL}'/>"""

            if nwfilter:
                if network.get("v6"):
                    xml += """<filterref filter='clean-traffic-ipv6'>"""
                else:
                    xml += """<filterref filter='clean-traffic'>"""

                if network.get("v4", {}).get("public", {}).get("primary"):
                    xml += f"""<parameter name='IP' value='{
                                network.get('v4', {}).get('public', {}).get('primary', {}).get('address')
                            }'/>"""

                if network.get("v4", {}).get("public", {}).get("secondary"):
                    xml += f"""<parameter name='IP' value='{
                                network.get('v4', {}).get('public', {}).get('secondary', {}).get('address')
                            }'/>"""

                if network.get("v6"):
                    xml += f"""<parameter name='IPV6' value='{
                                network.get('v6', {}).get('address')
                            }'/>"""

                xml += """</filterref>"""

            xml += """<model type='virtio'/>
                      </interface>
                    """

        # Create private pool device with IPv4
        if network.get("v4", {}).get("private"):
            xml += """<interface type='network'>"""

            if network.get("v4", {}).get("private", {}).get("mac"):
                xml += f"""<mac address='{network.get('v4', {}).get('private', {}).get('mac')}'/>"""

            if network.get("v4", {}).get("private", {}).get("pool"):
                xml += f"""<source network='{network.get('v4', {}).get('private', {}).get('pool')}'/>"""
            else:
                xml += f"""<source network='{settings.NETWORK_PRIVATE_POOL}'/>"""

            if nwfilter:
                xml += """<filterref filter='clean-traffic'>"""

                if network.get("v4", {}).get("private", {}):
                    xml += f"""<parameter name='IP' value='{
                                network.get('v4', {}).get('private', {}).get('address')
                            }'/>"""

                xml += """</filterref>"""

            xml += """<model type='virtio'/>
                      </interface>
                    """

        vnc_password = util.gen_password(length=8)
        xml += f"""<input type='mouse' bus='ps2'/>
                   <input type='tablet' bus='usb'/>
                   <graphics type='{display}' port='-1' autoport='yes' listen='0.0.0.0' passwd='{vnc_password}'>
                    <listen type='address' address='0.0.0.0'/>
                   </graphics>
                   <console type='pty'/>
                   <model type='cirrus' heads='1'>
                    <acceleration accel3d='yes' accel2d='yes'/>
                   </model>
                   <memballoon model='virtio'/>
                   </devices>
                   </domain>
                """

        self.defineXML(xml)

        if autostart:
            dom = self.get_instance(name)
            dom.setAutostart(1)


class wvmInstances(wvmConnect):
    def get_instance_status(self, name):
        inst = self.get_instance(name)
        return inst.info()[0]

    def get_instance_memory(self, name):
        inst = self.get_instance(name)
        mem = util.get_xml_data(inst.XMLDesc(), "currentMemory")
        return int(mem) / 1024

    def get_instance_vcpu(self, name):
        inst = self.get_instance(name)
        cur_vcpu = util.get_xml_data(inst.XMLDesc(), "vcpu", "current")
        if cur_vcpu:
            vcpu = cur_vcpu
        else:
            vcpu = util.get_xml_data(inst.XMLDesc(), "vcpu")
        return vcpu

    def get_instance_managed_save_image(self, name):
        inst = self.get_instance(name)
        return inst.hasManagedSaveImage()

    def get_uuid(self, name):
        inst = self.get_instance(name)
        return inst.UUIDString()

    def start(self, name):
        dom = self.get_instance(name)
        dom.create()

    def shutdown(self, name):
        dom = self.get_instance(name)
        dom.shutdown()

    def force_shutdown(self, name):
        dom = self.get_instance(name)
        dom.destroy()

    def managed_save(self, name):
        dom = self.get_instance(name)
        dom.managedSave(0)

    def managed_save_remove(self, name):
        dom = self.get_instance(name)
        dom.managedSaveRemove()

    def suspend(self, name):
        dom = self.get_instance(name)
        dom.suspend()

    def resume(self, name):
        dom = self.get_instance(name)
        dom.resume()

    def migrate(self, dconn, name, persist=False, undefine=False, disk=False):
        flags = 0
        dom = self.get_instance(name)
        if dom.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            flags += libvirt.VIR_MIGRATE_LIVE
            flags += libvirt.VIR_MIGRATE_COMPRESSED
        if persist:
            flags += libvirt.VIR_MIGRATE_PERSIST_DEST
        if undefine:
            flags += libvirt.VIR_MIGRATE_UNDEFINE_SOURCE
        if disk:
            flags += libvirt.VIR_MIGRATE_NON_SHARED_DISK
        dom_migrated = dom.migrate(dconn, flags)
        dom_migrated.setAutostart(1)


class wvmInstance(wvmConnect):
    def __init__(self, vname):
        wvmConnect.__init__(self)
        self.instance = self.get_instance(vname)

    def get_status(self):
        return self.instance.info()[0]

    def get_state(self, show_paused=False):
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            return "running"
        if self.get_status() == libvirt.VIR_DOMAIN_SHUTOFF:
            return "shutoff"
        if show_paused is True:
            if self.get_status() == libvirt.VIR_DOMAIN_PAUSED:
                return "paused"
        return "shutoff"

    def start(self):
        self.instance.create()

    def shutdown(self):
        self.instance.shutdown()

    def force_shutdown(self):
        self.instance.destroy()

    def reboot(self):
        self.instance.destroy()
        self.instance.create()

    def managed_save(self):
        self.instance.managedSave()

    def managed_save_remove(self):
        self.instance.managedSaveRemove()

    def check_managed_save_image(self):
        return self.instance.hasManagedSaveImage()

    def suspend(self):
        self.instance.suspend()

    def resume(self):
        self.instance.resume()

    def delete(self):
        self.instance.undefineFlags(libvirt.VIR_DOMAIN_UNDEFINE_SNAPSHOTS_METADATA)

    def XMLDesc(self, flag=0):
        return self.instance.XMLDesc(flag)

    def defineXML(self, xml):
        return self.wvm.defineXML(xml)

    def attachDevice(self, xml):
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            self.instance.attachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CURRENT)
            self.instance.attachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CONFIG)
        else:
            self.instance.attachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CONFIG)

    def detachDevice(self, xml):
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            self.instance.detachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CURRENT)
            self.instance.detachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CONFIG)
        else:
            self.instance.detachDeviceFlags(xml, libvirt.VIR_DOMAIN_AFFECT_CONFIG)

    def get_power_state(self):
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            return "active"
        if self.get_status() == libvirt.VIR_DOMAIN_PAUSED:
            return "suspend"
        if self.get_status() == libvirt.VIR_DOMAIN_SHUTOFF:
            return "inactive"

    def get_autostart(self):
        return self.instance.autostart()

    def set_autostart(self, flag):
        return self.instance.setAutostart(flag)

    def get_uuid(self):
        return self.instance.UUIDString()

    def get_vcpu(self):
        vcpu = util.get_xml_data(self.XMLDesc(), "vcpu")
        return int(vcpu)

    def get_cur_vcpu(self):
        cur_vcpu = util.get_xml_data(self.XMLDesc(), "vcpu", "current")
        if cur_vcpu:
            return int(cur_vcpu)

    def get_memory(self):
        mem = util.get_xml_data(self.XMLDesc(), "memory")
        return int(mem) * 1024

    def get_cur_memory(self):
        mem = util.get_xml_data(self.XMLDesc(), "currentMemory")
        return int(mem) * 1024

    def get_description(self):
        return util.get_xml_data(self.XMLDesc(), "description")

    def get_max_memory(self):
        return self.wvm.getInfo()[1] * (1024**2)

    def get_max_cpus(self):
        """Get number of physical CPUs."""
        hostinfo = self.wvm.getInfo()
        pcpus = hostinfo[4] * hostinfo[5] * hostinfo[6] * hostinfo[7]
        range_pcpus = range(1, int(pcpus + 1))
        return range_pcpus

    def get_net_ifaces(self):
        result = []

        def get_mac_ipaddr(xml, mac_host):
            tree = ElementTree.fromstring(xml)
            for net in tree.findall("ip/dhcp/host"):
                if net.get("mac") == mac_host:
                    return net.get("ip")
            return None

        tree = ElementTree.fromstring(self.XMLDesc())
        for interface in tree.findall("devices/interface"):
            ip_addr = None
            pool_name = None
            guest_mac = None
            guest_nic = None

            for dev in interface:
                if dev.tag == "mac":
                    guest_mac = dev.get("address")
                if dev.tag == "source":
                    pool_name = dev.get("network")
                    guest_nic = dev.get("network") or dev.get("bridge") or dev.get("dev")

            if pool_name:
                pool = self.get_network(pool_name)
                ip_addr = get_mac_ipaddr(pool.XMLDesc(), guest_mac)

            result.append({"ip": ip_addr, "mac": guest_mac, "nic": guest_nic, "pool": pool_name})

        return result

    def get_disk_device(self):
        result = []
        tree = ElementTree.fromstring(self.XMLDesc())
        for disks in tree.findall("devices/disk"):
            disk_img = None
            disk_dev = None
            disk_format = None

            if disks.get("device") == "disk":
                for dev in disks:
                    if dev.tag == "driver":
                        disk_format = dev.get("type")
                    if dev.tag == "source":
                        disk_img = dev.get("file") or dev.get("dev") or dev.get("name") or dev.get("volume")
                    if dev.tag == "target":
                        disk_dev = dev.get("dev")

                vol = self.get_volume_by_path(disk_img)
                stg = vol.storagePoolLookupByVolume()

                result.append(
                    {
                        "dev": disk_dev,
                        "name": vol.name(),
                        "pool": stg.name(),
                        "path": disk_img,
                        "format": disk_format,
                        "size": vol.info()[1],
                    }
                )

        return result

    def get_media_device(self):
        result = []
        tree = ElementTree.fromstring(self.XMLDesc())
        for media in tree.findall("devices/disk"):
            vol_name = None
            stg_name = None
            disk_img = None
            disk_dev = None

            if media.get("device") == "cdrom":
                for dev in media:
                    if dev.tag == "target":
                        disk_dev = dev.get("dev")
                    if dev.tag == "source":
                        disk_img = dev.get("file")

                if disk_dev and disk_img:
                    vol = self.get_volume_by_path(disk_img)
                    vol_name = vol.name()
                    stg = vol.storagePoolLookupByVolume()
                    stg_name = stg.name()

                result.append({"dev": disk_dev, "image": vol_name, "pool": stg_name, "path": disk_img})

        return result

    def umount_iso(self, dev, image_path):
        disk = """
            <disk type='file' device='cdrom'>
                <driver name='qemu' type='raw'/>
                <target dev='hda' bus='ide'/>
                <readonly/>
                <serial>0</serial>
              </disk>
        """

        tree = ElementTree.fromstring(self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE))
        for disk in tree.findall("devices/disk"):
            if disk.get("device") == "cdrom":
                disk_target = disk.find("target")
                if disk_target.get("dev") == dev:
                    disk_source = disk.find("source")
                    if disk_source.get("file") == image_path:
                        disk.remove(disk_source)
                        if disk.find("backingStore"):
                            disk.remove(disk.find("backingStore"))
                        break

        xmldev = ElementTree.tostring(disk).decode()
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            self.updateDevice(xmldev, live=True)
            xmldom = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)

        if self.get_status() == libvirt.VIR_DOMAIN_SHUTOFF:
            self.updateDevice(xmldev, live=False)
            xmldom = ElementTree.tostring(tree).decode()

        self.defineXML(xmldom)

    def cpu_usage(self):
        usage = {"user": 0, "total": 0, "system": 0}
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            nbcore = self.instance.info()[3]
            stats = self.instance.getCPUStats(True)
            user_ago = stats[0]["user_time"]
            total_ago = stats[0]["cpu_time"]
            system_ago = stats[0]["system_time"]

            time.sleep(1)
            stats = self.instance.getCPUStats(True)
            user_now = stats[0]["user_time"]
            total_now = stats[0]["cpu_time"]
            system_now = stats[0]["system_time"]

            diff_user = user_now - user_ago
            diff_total = total_now - total_ago
            diff_system = system_now - system_ago

            usage["user"] = 100 * diff_user / (nbcore * (10**9))
            usage["total"] = 100 * diff_total / (nbcore * (10**9))
            usage["system"] = 100 * diff_system / (nbcore * (10**9))

            if usage["user"] > 100:
                usage["user"] = 100
            if usage["total"] > 100:
                usage["total"] = 100
            if usage["system"] > 100:
                usage["system"] = 100
        return usage

    def disk_usage(self):
        usage = []
        devices = []
        rd_diff_usage = 0
        wr_diff_usage = 0
        tree = ElementTree.fromstring(self.XMLDesc())
        for disk in tree.findall("devices/disk"):
            if disk.get("device") == "disk":
                dev_file = None
                dev_bus = None
                network_disk = True
                for elm in disk:
                    if elm.tag == "source":
                        if elm.get("protocol"):
                            dev_file = elm.get("protocol")
                            network_disk = True
                        if elm.get("file"):
                            dev_file = elm.get("file")
                        if elm.get("dev"):
                            dev_file = elm.get("dev")
                    if elm.tag == "target":
                        dev_bus = elm.get("dev")
                if (dev_file and dev_bus) is not None:
                    if network_disk:
                        dev_file = dev_bus
                    devices.append([dev_file, dev_bus])
        for dev in devices:
            if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
                rd_use_ago = self.instance.blockStats(dev[0])[1]
                wr_use_ago = self.instance.blockStats(dev[0])[3]

                time.sleep(1)
                rd_use_now = self.instance.blockStats(dev[0])[1]
                wr_use_now = self.instance.blockStats(dev[0])[3]

                rd_diff_usage = rd_use_now - rd_use_ago
                wr_diff_usage = wr_use_now - wr_use_ago
            usage.append({"dev": dev[1], "rd": rd_diff_usage, "wr": wr_diff_usage})
        return usage

    def net_usage(self):
        usage = []
        devices = []
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            targets = util.get_xml_findall(self.XMLDesc(), "devices/interface/target")
            for target in targets:
                devices.append(target.get("dev"))
            for i, dev in enumerate(devices):
                rx_use_ago = self.instance.interfaceStats(dev)[0]
                tx_use_ago = self.instance.interfaceStats(dev)[4]

                time.sleep(1)
                rx_use_now = self.instance.interfaceStats(dev)[0]
                tx_use_now = self.instance.interfaceStats(dev)[4]

                rx_diff_usage = (rx_use_now - rx_use_ago) * 8
                tx_diff_usage = (tx_use_now - tx_use_ago) * 8
                usage.append({"dev": i, "rx": rx_diff_usage, "tx": tx_diff_usage})
        else:
            for i, dev in enumerate(self.get_net_device()):
                usage.append({"dev": i, "rx": 0, "tx": 0})
        return usage

    def get_telnet_port(self):
        telnet_port = None
        service_port = None
        consoles = util.get_xml_findall(self.XMLDesc(), "devices/console")
        for console in consoles:
            if console.get("type") == "tcp":
                for elm in console:
                    if elm.tag == "source":
                        if elm.get("service"):
                            service_port = elm.get("service")
                    if elm.tag == "protocol":
                        if elm.get("type") == "telnet":
                            if service_port is not None:
                                telnet_port = service_port
        return telnet_port

    def get_console_listen_addr(self):
        listen_addr = util.get_xml_data(self.XMLDesc(), "devices/graphics", "listen")
        if listen_addr is None:
            listen_addr = util.get_xml_data(self.XMLDesc(), "devices/graphics/listen", "address")
            if listen_addr is None:
                return "127.0.0.1"
        return listen_addr

    def get_console_socket(self):
        return util.get_xml_data(self.XMLDesc(), "devices/graphics", "socket")

    def get_console_type(self):
        return util.get_xml_data(self.XMLDesc(), "devices/graphics", "type")

    def set_console_type(self, console_type):
        current_type = self.get_console_type()
        if current_type == console_type:
            return True
        if console_type == "" or console_type not in DISPLAY:
            return False
        xml = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        root = ElementTree.fromstring(xml)
        try:
            graphic = root.find(f"devices/graphics[@type='{current_type}']")
        except SyntaxError:
            # Little fix for old version ElementTree
            graphic = root.find("devices/graphics")
        graphic.set("type", console_type)
        newxml = ElementTree.tostring(root)
        self.defineXML(newxml)

    def get_console_port(self, console_type=None):
        if console_type is None:
            console_type = self.get_console_type()
        return util.get_xml_data(self.XMLDesc(), f"devices/graphics[@type='{console_type}']", "port")

    def get_console_websocket_port(self):
        console_type = self.get_console_type()
        return util.get_xml_data(self.XMLDesc(), f"devices/graphics[@type='{console_type}']", "websocket")

    def get_console_passwd(self):
        return util.get_xml_data(self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE), "devices/graphics", "passwd")

    def set_console_passwd(self, passwd):
        xml = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        root = ElementTree.fromstring(xml)
        console_type = self.get_console_type()
        try:
            graphic = root.find(f"devices/graphics[@type='{console_type}']")
        except SyntaxError:
            # Little fix for old version ElementTree
            graphic = root.find("devices/graphics")
        if graphic is None:
            return False
        if passwd:
            graphic.set("passwd", passwd)
        else:
            try:
                graphic.attrib.pop("passwd")
            except ElementTree:
                pass
        newxml = ElementTree.tostring(root)
        return self.defineXML(newxml)

    def set_console_keymap(self, keymap):
        xml = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        root = ElementTree.fromstring(xml)
        console_type = self.get_console_type()
        try:
            graphic = root.find(f"devices/graphics[@type='{console_type}']")
        except SyntaxError:
            # Little fix for old version ElementTree
            graphic = root.find("devices/graphics")
        if keymap:
            graphic.set("keymap", keymap)
        else:
            try:
                graphic.attrib.pop("keymap")
            except ElementTree:
                pass
        newxml = ElementTree.tostring(root)
        self.defineXML(newxml)

    def get_console_keymap(self):
        return util.get_xml_data(self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE), "devices/graphics", "keymap") or ""

    def resize_resources(self, vcpu, memory, current_vcpu=None, current_memory=None):
        """
        Function change ram and cpu on vds.
        """
        memory = round(memory / 1024)
        if current_memory is None:
            current_memory = memory
        else:
            current_memory = round(current_memory / 1024)
        self.instance.setMaxMemory(memory)
        self.instance.setMemoryFlags(current_memory, libvirt.VIR_DOMAIN_AFFECT_CONFIG)

        if current_vcpu is None:
            current_vcpu = vcpu
        vcpu_flags = libvirt.VIR_DOMAIN_VCPU_MAXIMUM + libvirt.VIR_DOMAIN_AFFECT_CONFIG
        self.instance.setVcpusFlags(vcpu, vcpu_flags)
        self.instance.setVcpusFlags(current_vcpu, libvirt.VIR_DOMAIN_VCPU_CURRENT)

    def add_private_iface(self, ipaddr, net_pool, mac=None):
        xml = """<interface type='network'>"""
        if mac:
            xml += f"""<mac address='{mac}'/>"""
        xml += f"""<source network='{net_pool}'/>
                  <model type='virtio'/>
                  <filterref filter='clean-traffic'>
                     <parameter name='IP' value='{ipaddr}'/>
                  </filterref>
                  </interface>"""
        self.attachDevice(xml)

    def add_rbd_disk(self, path, hosts, username, uuid, dev="vdb"):
        xml = f"""<disk type='network' path='disk'>
                    <driver name='qemu' type='raw' cache='writeback'/>
                    <source protocol='rbd' name='{path}'>"""
        for host in hosts:
            xml += f"""<host name='{host}' port='6789'/>"""
        xml += f"""</source>
                     <auth username='{username}'>
                        <secret type='ceph' uuid='{uuid}'/>
                    </auth>
                    <target dev='{dev}' bus='virtio'/>
                  </disk>"""
        self.attachDevice(xml)

    def del_rbd_disk(self):
        xml = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        tree = ElementTree.fromstring(xml)
        for disk in tree.findall("devices/disk"):
            if disk.get("type") == "network":
                xml_disk = ElementTree.tostring(disk)
                self.detachDevice(xml_disk.decode())

    def get_iso_media(self):
        iso = []
        storages = self.get_storages()
        for storage in storages:
            stg = self.get_storage(storage)
            if stg.info()[0] != 0:
                try:
                    stg.refresh(0)
                except libvirt.libvirtError:
                    pass
                for img in stg.listVolumes():
                    if img.endswith(".iso"):
                        iso.append(img)
        return iso

    def delete_disk(self, dev=None):
        disks = self.get_disk_device()
        if dev:
            for disk in disks:
                if disk["dev"] == dev:
                    vol = self.get_volume_by_path(disk.get("path"))
                    vol.delete(0)
        else:
            for disk in disks:
                vol = self.get_volume_by_path(disk.get("path"))
                vol.delete(0)

    def _snapshotCreateXML(self, xml, flag):
        self.instance.snapshotCreateXML(xml, flag)

    def create_snapshot(self, name):
        xml_dom = self.XMLDesc()
        rbd_disk = False
        tree = ElementTree.fromstring(xml_dom)
        for disk in tree.findall("devices/disk"):
            if disk.get("type") == "network":
                xml_disk = ElementTree.tostring(disk)
                rbd_disk = True
        if rbd_disk:
            self.detachDevice(xml_disk)
        xml = f"""<domainsnapshot>
                     <name>{name}</name>
                     <state>shutoff</state>
                     <creationTime>{time.time():d}</creationTime>
                     <memory snapshot='no'/>"""
        xml += self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        xml += """</domainsnapshot>"""
        self._snapshotCreateXML(xml, 0)
        if rbd_disk:
            self.attachDevice(xml_disk)

    def get_snapshot(self):
        snapshots = []
        snapshot_list = self.instance.snapshotListNames(0)
        for snapshot in snapshot_list:
            snap = self.instance.snapshotLookupByName(snapshot, 0)
            snap_time_create = util.get_xml_data(snap.getXMLDesc(), "creationTime")
            snapshots.append({"date": datetime.fromtimestamp(int(snap_time_create)), "name": snapshot})
        return snapshots

    def snapshot_delete(self, snapshot):
        snap = self.instance.snapshotLookupByName(snapshot, 0)
        snap.delete(0)

    def snapshot_revert(self, snapshot):
        xml_dom = self.XMLDesc()
        rbd_disk = False
        tree = ElementTree.fromstring(xml_dom)
        for disk in tree.findall("devices/disk"):
            if disk.get("type") == "network":
                xml_disk = ElementTree.tostring(disk)
                rbd_disk = True
        if rbd_disk:
            self.detachDevice(xml_disk)
        snap = self.instance.snapshotLookupByName(snapshot, 0)
        self.instance.revertToSnapshot(snap, 0)
        if rbd_disk:
            self.attachDevice(xml_disk)

    def get_managed_save_image(self):
        return self.instance.hasManagedSaveImage(0)

    def clone_instance(self, clone_data):
        clone_dev_path = []
        xml = self.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
        tree = ElementTree.fromstring(xml)
        name = tree.find("name")
        name.text = clone_data["name"]
        uuid = tree.find("uuid")
        tree.remove(uuid)

        for num, net in enumerate(tree.findall("devices/interface")):
            elm = net.find("mac")
            elm.set("address", clone_data[f"net-{str(num)}"])

        for disk in tree.findall("devices/disk"):
            if disk.get("device") == "disk":
                elm = disk.find("target")
                device_name = elm.get("dev")
                if device_name:
                    target_file = clone_data[f"disk-{device_name}"]
                    try:
                        meta_prealloc = clone_data[f"meta-{device_name}"]
                    except Exception:
                        meta_prealloc = False
                    elm.set("dev", device_name)

                elm = disk.find("source")
                source_file = elm.get("file")
                if source_file:
                    clone_dev_path.append(source_file)
                    clone_path = os.path.join(os.path.dirname(source_file), target_file)
                    elm.set("file", clone_path)

                    vol = self.get_volume_by_path(source_file)
                    vol_format = util.get_xml_data(vol.XMLDesc(), "target/format", "type")

                    if vol_format == "qcow2" and meta_prealloc:
                        meta_prealloc = True
                    vol_clone_xml = f"""
                                    <volume>
                                        <name>{target_file}</name>
                                        <capacity>0</capacity>
                                        <allocation>0</allocation>
                                        <target>
                                            <format type='{vol_format}'/>
                                        </target>
                                    </volume>"""
                    stg = vol.storagePoolLookupByVolume()
                    stg.createXMLFrom(vol_clone_xml, vol, meta_prealloc)

        self.defineXML(ElementTree.tostring(tree))

    def migrate(self, dconn, persist=False, undefine=False, disk=False):
        flags = 0
        if self.get_status() == libvirt.VIR_DOMAIN_RUNNING:
            flags += libvirt.VIR_MIGRATE_LIVE
        if persist:
            flags += libvirt.VIR_MIGRATE_PERSIST_DEST
        if undefine:
            flags += libvirt.VIR_MIGRATE_UNDEFINE_SOURCE
        if disk:
            flags += libvirt.VIR_MIGRATE_NON_SHARED_DISK
        dom = self.instance.migrate(dconn, flags)
        dom.setAutostart(1)
