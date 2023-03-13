"""
WebVirtCloud daemon for managing VM's filesystem.

"""
import configparser
from optparse import OptionParser


# HostVirtMgr options
parser = OptionParser()
parser.add_option("-c", "--conf", dest="config", action="store", help="Config file path", default="webvirtcompute.ini")
(options, args) = parser.parse_args()

# Config file
conf = configparser.ConfigParser()
conf.read(options.config)

# Token settings
TOKEN = conf.get("daemon", "token", fallback="")

# Daemon settings
PORT = conf.getint("daemon", "port", fallback=8884)
HOST = conf.get("daemon", "host", fallback="0.0.0.0")

# Metrics settings
METRICS_URL = conf.get("metrics", "url", fallback="http://localhost:9090/api/v1/query_range")

# Cache path
CACHE_DIR = conf.get("cache", "directory", fallback="/var/lib/libvirt/template_cache")

# External bridge name
BRIDGE_EXT = conf.get("bridge", "external", fallback="br-ext")

# Storage pools
STORAGE_IMAGE_POOL = conf.get("storage", "image_pool", fallback="images")
STORAGE_BACKUP_POOL = conf.get("storage", "bakup_pool", fallback="backups")
STORAGE_VOLUME_POOL = conf.get("storage", "volume_pool", fallback="volumes")

# Network pools
NETWORK_PUBLIC_POOL = conf.get("network", "public_pool", fallback="public")
NETWORK_PRIVATE_POOL = conf.get("network", "private_pool", fallback="private")

# Backup settings
BACKUP_USER = conf.get("backup", "user", fallback="virtmgr")
BACKUP_KEY_FILE = conf.get("backup", "file", fallback="/etc/webvirtcompute/privkey.pem")

# Firewall rule name
FIREWALL_IN_NAME = conf.get("firewall", "in_name", fallback="FW_I_")
FIREWALL_OUT_NAME = conf.get("firewall", "out_name", fallback="FW_O_")

# Firewall insert after line
FIREWALL_INSERT_LINE = conf.getint("firewall", "insert_line", fallback=2)

# Firewall prefix
FIREWALL_CHAIN_PREFIX = conf.get("firewall", "chain_prefix", fallback="")

# Firewalld settings
FIREWALLD_STATE_TIMEOUT = conf.getint("firewall", "state_timeout", fallback=120)
FIREWALLD_STATE_FILE = conf.get("firewall", "state_file", fallback="/var/run/firewalld/locked")
