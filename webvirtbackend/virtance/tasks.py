from uuid import uuid4
from django.conf import settings
from webvirtcloud.celery import app
from passlib.hash import sha512_crypt

from compute.helper import assign_free_compute, WebVirtCompute
from network.helper import (
    assign_free_ipv4_public,
    assign_free_ipv4_compute,
    assign_free_ipv4_private,
)
from compute.models import Compute
from network.models import Network, IPAddress
from keypair.models import KeyPairVirtance
from .models import Virtance


@app.task
def create_virtance(virtance_id, password):
    keypairs = []
    compute = None
    ipv4_public = None
    ipv4_compute = None
    ipv4_private = None
    virtance = Virtance.objects.get(id=virtance_id)
    password = password if password else uuid4().hex[0:24]
    password_hash = sha512_crypt.encrypt(password, salt=uuid4().hex[0:8], rounds=5000)

    if assign_free_compute(virtance.id) is True:
        compute = Compute.objects.get(virtance=virtance)

    if assign_free_ipv4_compute(virtance.id) is True:
        ipv4_compute = IPAddress.objects.get(network__type=Network.COMPUTE, virtance=virtance)

    if assign_free_ipv4_public(virtance.id) is True:
        ipv4_public = IPAddress.objects.get(network__type=Network.PUBLIC, virtance=virtance)

    if assign_free_ipv4_private(virtance.id) is True:
        ipv4_private = IPAddress.objects.get(network__type=Network.PRIVATE, virtance=virtance)

    for kpv in KeyPairVirtance.objects.filter(virtance=virtance):
        keypairs.append(kpv.keypair.public_key)
        
    if compute and ipv4_public and ipv4_compute and ipv4_private:
        images = [
            {
                "name": settings.VM_NAME_PREFIX + str(virtance.id),
                "size": virtance.size.disk,
                "url": f"{settings.PUBLIC_IMAGES_URL}{virtance.image.file_name}",
                "md5sum": virtance.image.md5sum,
                "primary": True
            }
        ]
        network = {
            "v4": {
                "public": {
                    "primary": {
                        "address": ipv4_public.address,
                        "gateway": ipv4_public.network.gateway,
                        "netmask": ipv4_public.network.netmask,
                        "dns1": ipv4_public.network.dns1,
                        "dns2": ipv4_public.network.dns2
                        
                    },
                    "secondary": {
                        "address": ipv4_compute.address,
                        "gateway": ipv4_compute.network.gateway,
                        "netmask": ipv4_compute.network.netmask
                    }
                },
                "private": {
                    "address": ipv4_private.address,
                    "gateway": ipv4_private.network.gateway,
                    "netmask": ipv4_private.network.netmask
                }
            },
            "v6": None
        }
        wvcomp = WebVirtCompute(compute.token, compute.hostname)
        wvcomp.create_virtance(
            virtance.id,
            virtance.uuid.hex,
            virtance.name,
            virtance.size.vcpu,
            virtance.size.memory,
            images, 
            network, 
            keypairs,
            password_hash,
        )

@app.task
def action_virtance(virtance_id, action):
    virtance = Virtance.objects.get(id=virtance_id)
    wvcomp = WebVirtCompute(virtance.compute.token, virtance.compute.hostname)
    wvcomp.action_virtance(virtance.id, action)

@app.task
def delete_virtance(virtance_id):
    virtance = Virtance.objects.get(id=virtance_id)
    wvcomp = WebVirtCompute(virtance.compute.token, virtance.compute.hostname)
    deleted = wvcomp.delete_virtance(virtance.id)
    if deleted is True:
        ipaddresse = IPAddress.objects.filter(virtance=virtance)
        ipaddresse.delete()
        virtance.delete()
