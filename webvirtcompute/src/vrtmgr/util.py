import random
import libvirt
import hashlib
from xml.etree import ElementTree
from string import ascii_letters, digits


def is_kvm_available(xml):
    tree = ElementTree.fromstring(xml)
    for dom in tree.findall("guest/arch/domain"):
        if "kvm" in dom.get("type"):
            return True
    return False


def randomMAC():
    """Generate a random MAC address."""
    # qemu MAC
    oui = [0x52, 0x54, 0x00]

    mac = oui + [random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF)]
    return ":".join(map(lambda x: "%02x" % x, mac))


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


def randomUUID():
    """Generate a random UUID."""

    u = [random.randint(0, 255) for dummy in range(0, 16)]
    return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2, "%02x" * 6]) % tuple(u)


def get_max_vcpus(conn, type=None):
    """@param conn: libvirt connection to poll for max possible vcpus
    @type type: optional guest type (kvm, etc.)"""
    if type is None:
        type = conn.getType()
    try:
        m = conn.getMaxVcpus(type.lower())
    except libvirt.libvirtError:
        m = 32
    return m


def xml_escape(str):
    """Replaces chars ' " < > & with xml safe counterparts"""
    if str is None:
        return None

    str = str.replace("&", "&amp;")
    str = str.replace("'", "&apos;")
    str = str.replace('"', "&quot;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    return str


def compareMAC(p, q):
    """Compare two MAC addresses"""
    pa = p.split(":")
    qa = q.split(":")

    if len(pa) != len(qa):
        if p > q:
            return 1
        else:
            return -1

    for i in range(len(pa)):
        n = int(pa[i], 0x10) - int(qa[i], 0x10)
        if n > 0:
            return 1
        elif n < 0:
            return -1
    return 0


def get_xml_data(xml, path=None, element=None):
    res = ""
    if not path and not element:
        return ""

    tree = ElementTree.fromstring(xml)
    if path:
        child = tree.find(path)
        if child is not None:
            if element:
                res = child.get(element)
            else:
                res = child.text
    else:
        res = tree.get(element)
    return res


def get_xml_findall(xml, string):
    tree = ElementTree.fromstring(xml)
    return tree.findall(string)


def pretty_mem(val):
    val = int(val)
    if val > (10 * 1024 * 1024):
        return "%2dGB" % (val / (1024.0 * 1024.0))
    else:
        return "%2dMB" % (val / 1024.0)


def pretty_bytes(val):
    val = int(val)
    if val > (1024 * 1024 * 1024):
        return "%2.2f GB" % (val / (1024.0 * 1024.0 * 1024.0))
    else:
        return "%2.2f MB" % (val / (1024.0 * 1024.0))


def gen_password(length=24, symbols=False):
    simple_symbols = ""
    if symbols:
        simple_symbols = "!@#$%^&*()_+[]-=:;{}?|<>"
    password = "".join([random.choice(ascii_letters + simple_symbols + digits) for dummy in range(length)])
    return password
