from typing import Optional
from pydantic import BaseModel


class VirtanceCreate(BaseModel):
    uuid: str
    name: str
    hostname: str
    vcpu: int
    memory: int
    images: list
    network: dict
    keypairs: list
    root_password: str


class VirtanceStatus(BaseModel):
    action: str


class VirtanceResize(BaseModel):
    vcpu: int
    memory: int
    disk_size: Optional[int] = None


class VirtanceMedia(BaseModel):
    image: str
    device: str


class StorageCreate(BaseModel):
    name: str
    type: str
    target: Optional[str] = None
    source: Optional[str] = None
    user: Optional[str] = None
    pool: Optional[str] = None
    host: Optional[str] = None
    host2: Optional[str] = None
    host3: Optional[str] = None
    format: Optional[str] = None
    secret: Optional[str] = None


class StorageAction(BaseModel):
    action: str


class VolumeCreate(BaseModel):
    name: str
    size: int
    format: Optional[str] = None


class VolumeAction(BaseModel):
    action: str
    name: Optional[str] = None
    size: Optional[int] = None


class NetworkCreate(BaseModel):
    name: str
    forward: str
    gateway: Optional[str] = None
    mask: Optional[str] = None
    dhcp: Optional[str] = None
    bridge: Optional[str] = None
    openvswitch: Optional[str] = None
    fixed: Optional[str] = None


class NetworkAction(BaseModel):
    action: str


class SecretCreate(BaseModel):
    type: str
    data: str
    private: str
    ephemeral: str


class SecretValue(BaseModel):
    value: str


class NwFilterCreate(BaseModel):
    xml: str


class FloatingIPs(BaseModel):
    fixed_address: str
    address: str
    prefix: str
    gateway: str


class ResetPassword(BaseModel):
    distro: str
    password: str
