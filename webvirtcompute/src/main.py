import requests
from typing import Optional
from libvirt import libvirtError
from fastapi import status, FastAPI, Depends, Response

from vrtmgr import libvrt
from vrtmgr import images
from vrtmgr import network
from auth import basic_auth
from execption import raise_error_msg
from settings import METRICS_URL, STORAGE_IMAGE_POOL
from model import VirtanceCreate, VirtanceStatus, VirtanceResize, VirtanceMedia
from model import StorageCreate, StorageAction, VolumeCreate, VolumeAction, NwFilterCreate
from model import NetworkCreate, NetworkAction, SecretCreate, SecretValue, FloatingIPs, ResetPassword


app = FastAPI(dependencies=[Depends(basic_auth)])


@app.get("/metrics/", status_code=status.HTTP_200_OK)
def metrics(query: Optional[str] = "", start: Optional[str] = "", end: Optional[str] = "", step: Optional[str] = ""):
    params = {"query": query, "start": start, "end": end, "step": step}
    responce = requests.get(METRICS_URL, params=params).json()
    return responce


@app.post("/virtances/", response_model=VirtanceCreate, status_code=status.HTTP_201_CREATED)
def virtance_create(virtance: VirtanceCreate):
    # Download and deploy images template
    for img in virtance.images:
        if img.get("primary") is True:
            template = images.Template(img.get("url"), img.get("md5sum"))
            err_msg = template.download()
            if err_msg is None:
                image = images.Image(img.get("name"), STORAGE_IMAGE_POOL)
                err_msg = image.deploy_template(
                    template_path=template.path,
                    disk_size=img.get("size"),
                    networks=virtance.network,
                    public_keys=virtance.keypairs,
                    hostname=virtance.hostname,
                    root_password=virtance.root_password,
                )
        else:
            try:
                conn = libvrt.wvmStorage(STORAGE_IMAGE_POOL)
                conn.create_volume(img.get("name"), img.get("size"), fmt="raw")
                conn.close()
            except libvirtError as err:
                raise_error_msg(err)

    if err_msg is not None:
        raise_error_msg(err_msg)

    # Create XML
    try:
        conn = libvrt.wvmCreate()
        conn.create_xml(
            virtance.name, 
            virtance.vcpu, 
            virtance.memory, 
            virtance.images, 
            virtance.network, 
            uuid=virtance.uuid
        )
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    # Run VM
    try:
        conn = libvrt.wvmInstance(virtance.name)
        conn.start()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return virtance


@app.get("/virtances/", status_code=status.HTTP_200_OK)
def virtances():
    virtances = []

    try:
        conn = libvrt.wvmConnect()
        virtance_names = conn.get_instances()
        conn.close()
        
        for name in virtance_names:
            dconn = libvrt.wvmInstance(name)
            virtances.append(
                {
                    "name": name,
                    "status": dconn.get_state(),
                    "uuid": dconn.get_uuid(),
                    "vcpu": dconn.get_vcpu(),
                    "memory": dconn.get_memory(),
                    "disks": dconn.get_disk_device(),
                    "media": dconn.get_media_device(),
                    "ifaces": dconn.get_net_ifaces(),
                }
            )
            dconn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"virtances": virtances}


@app.get("/virtances/{name}/", status_code=status.HTTP_200_OK)
def virtance_info(name):
    try:
        conn = libvrt.wvmInstance(name)
        response = {
            "name": name,
            "uuid": conn.get_uuid(),
            "vcpu": conn.get_vcpu(),
            "disks": conn.get_disk_device(),
            "media": conn.get_media_device(),
            "status": conn.get_state(),
            "memory": conn.get_memory(),
            "ifaces": conn.get_net_ifaces(),
        }
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"virtances": response}


@app.get("/virtances/{name}/status/", status_code=status.HTTP_200_OK)
def virtance(name):
    try:
        conn = libvrt.wvmInstance(name)
        status = conn.get_state()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return {"status": status}


@app.post("/virtances/{name}/status/", response_model=VirtanceStatus, status_code=status.HTTP_200_OK)
def virtance_status(name, status: VirtanceStatus):

    if status.action not in ["power_on", "power_off", "shutdown", "reboot", "suspend", "resume"]:
        raise_error_msg("Status does not exist.")

    try:
        conn = libvrt.wvmInstance(name)
        if status.action == "power_on":
            conn.start()
        if status.action == "power_off":
            conn.force_shutdown()
        if status.action == "shutdown":
            conn.shutdown()
        if status.action == "reboot":
            conn.reboot()
        if status.action == "suspend":
            conn.suspend()
        if status.action == "resume":
            conn.resume()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return status


@app.post("/virtances/{name}/resize/", response_model=VirtanceResize, status_code=status.HTTP_200_OK)
def virtance_resize(name, resize: VirtanceResize):
    try:
        conn = libvrt.wvmInstance(name)
        if conn.get_state() != "shutoff":
            raise_error_msg("Please shutoff the virtual machine.")
        conn.resize_resources(resize.vcpu, resize.memory)
        if resize.disk_size:
            drivers = conn.get_disk_device()
            for drive in drivers:
                if drive.get("dev") == "vda" or drive.get("dev") == "sda":
                    sconn = libvrt.wvmStorage(drive.get("pool"))
                    sconn.resize_volume(drive.get("name"), resize.disk_size)
                    sconn.close()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return resize


@app.get("/virtances/{name}/media/", status_code=status.HTTP_200_OK)
def virtance_media_info(name):
    try:
        conn = libvrt.wvmInstance(name)
        media = conn.get_media_device()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return {"media": media}


@app.post("/virtances/{name}/media/", response_model=VirtanceMedia, status_code=status.HTTP_200_OK)
def virtance_media_mount(name, media: VirtanceMedia):
    try:
        conn = libvrt.wvmInstance(name)
        conn.mount_iso(media.device, media.image)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return media


@app.delete("/virtances/{name}/media/", response_model=VirtanceMedia)
def virtance_media_umount(name, media: VirtanceMedia):
    try:
        conn = libvrt.wvmInstance(name)
        conn.umount_iso(media.device, media.image)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/virtances/{name}/reset_password/", response_model=ResetPassword, status_code=status.HTTP_200_OK)
def virtance_reset_password(name, reset_pass: ResetPassword):
    raise_error_msg = None

    try:
        conn = libvrt.wvmInstance(name)
        drives = conn.get_disk_device()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    try:
        image = images.Image(drives[0].get("name"), drives[0].get("pool"))
        err_msg = image.reset_password(reset_pass.get("distro"), reset_pass.get("password"))
    except Exception as err:
        raise_error_msg(err)

    if err_msg:
        raise_error_msg(err_msg)

    return reset_pass


@app.delete("/virtances/{name}/")
def virtance_detele(name):
    try:
        dom = libvrt.wvmInstance(name)
        dom.force_shutdown()
        drives = dom.get_disk_device()
        for drive in drives:
            if drive.get("dev") == "vda" or drive.get("dev") == "sda":
                stg = libvrt.wvmStorage(drive.get("pool"))
                vol = stg.get_volume(drive.get("name"))
                vol.delete()
                stg.refresh()
                stg.close()
        dom.delete()
        dom.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/host/", status_code=status.HTTP_200_OK)
def host():
    conn = libvrt.wvmConnect()
    host = conn.get_host_info()
    cpu = conn.get_host_cpu_usage()
    memory = conn.get_host_mem_usage()
    conn.close()
    
    return {"host": host, "memory": memory, "cpu": cpu}


@app.get("/storages/", status_code=status.HTTP_200_OK)
def storages():
    conn = libvrt.wvmStorages()
    storages = conn.get_storages_info()
    conn.close()
    
    return {"storages": storages}


@app.post("/storages/", response_model=StorageCreate, status_code=status.HTTP_201_CREATED)
def storages_list(pool: StorageCreate):
    conn = libvrt.wvmStorages()
    
    if pool.type == "dir":
        if pool.target is None:
            raise_error_msg("Target field required for dir storage pool.")
        try:
            conn.create_storage_dir(
                pool.name,
                pool.target,
            )
        except libvirtError as err:
            raise_error_msg(err)
    
    if pool.type == "logical":
        if pool.source is None:
            raise_error_msg("Source field required for dir storage pool.")
        try:
            conn.create_storage_logic(
                pool.name,
                pool.source,
            )
        except libvirtError as err:
            raise_error_msg(err)
    
    if pool.type == "rbd":
        if pool.source is None and pool.pool is None and pool.secret is None and pool.host is None:
            raise_error_msg("Source, pool, secret and host fields required for rbd storage pool.")
        try:
            conn.create_storage_ceph(
                pool.name, pool.pool, pool.user, pool.secret, pool.host, pool.host2, pool.host3
            )
        except libvirtError as err:
            raise_error_msg(err)
    
    if pool.type == "nfs":
        if pool.host is None and pool.source is None and pool.format is None and pool.target is None:
            raise_error_msg("Pool, source, source and target fields required for nfs storage pool.")
        try:
            conn.create_storage_netfs(pool.name, pool.host, pool.source, pool.format, pool.target)
        except libvirtError as err:
            raise_error_msg(err)

    conn.close()
    
    return pool


@app.get("/storages/{pool}/", status_code=status.HTTP_200_OK)
def storage_info(pool):
    try:
        conn = libvrt.wvmStorage(pool)
    except libvirtError as err:
        raise_error_msg(err)

    storage = {
        "name": pool,
        "active": conn.get_active(),
        "type": conn.get_type(),
        "volumes": conn.get_volumes_info(),
        "size": {"total": conn.get_total_size(), "used": conn.get_used_size(), "free": conn.get_free_size()},
        "autostart": conn.get_autostart(),
    }
    conn.close()
    
    return {"storage": storage}


@app.post("/storages/{pool}/", response_model=StorageAction, status_code=status.HTTP_200_OK)
def storage_action(pool, stg: StorageAction):
    if stg.action not in ["start", "stop", "autostart", "manualstart"]:
        raise_error_msg("Action not exist.")

    try:
        conn = libvrt.wvmStorage(pool)
        if stg.action == "start":
            conn.start()
        if stg.action == "stop":
            conn.stop()
        if stg.action == "autostart":
            conn.set_autostart(True)
        if stg.action == "manualstart":
            conn.set_autostart(False)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return stg


@app.delete("/storages/{pool}/")
def storage_delete(pool):
    try:
        conn = libvrt.wvmStorage(pool)
        conn.stop()
        conn.delete()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/storages/{pool}/volumes/", status_code=status.HTTP_200_OK)
def storage_volume_list(pool):
    try:
        conn = libvrt.wvmStorage(pool)
        volumes = conn.get_volumes_info()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"volumes": volumes}


@app.post("/storages/{pool}/volumes/", response_model=VolumeCreate, status_code=status.HTTP_201_CREATED)
def storage_volume_create(pool, volume: VolumeCreate):
    try:
        conn = libvrt.wvmStorage(pool)
        conn.create_volume(name=volume.name, size=volume.size * (1024**3), fmt=volume.format)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return volume


@app.get("/storages/{pool}/volumes/{volume}/", status_code=status.HTTP_200_OK)
def storage_volume_info(pool, volume):
    try:
        conn = libvrt.wvmStorage(pool)
        volomue_data = conn.get_volume_info(volume)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"volume": volomue_data}


@app.post("/storages/{pool}/volumes/{volume}/", response_model=VolumeAction, status_code=status.HTTP_200_OK)
def storage_volume_action(pool, volume, val: VolumeAction):
    if val.action not in ["resize", "clone"]:
        raise_error_msg("Action not exist.")
    
    try:
        conn = libvrt.wvmStorage(pool)
        conn.get_volume(volume)

        if val.action == "resize":
            if not val.size:
                raise_error_msg("Size required for resize ation.")
            try:
                conn.resize_volume(val.size)
            except libvirtError as err:
                raise_error_msg(err)

        if val.action == "clone":
            if not val.name:
                raise_error_msg("Name required for clone ation.")
            try:
                conn.clone_volume(volume, val.name)
            except libvirtError as err:
                raise_error_msg(err)

        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return val


@app.delete("/storages/{pool}/volumes/{volume}/")
def storage_volume_delete(pool, volume):
    try:
        conn = libvrt.wvmStorage(pool)
        conn.del_volume(volume)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/networks/", status_code=status.HTTP_200_OK)
def networks_list():
    conn = libvrt.wvmNetworks()
    networks = conn.get_networks_info()
    conn.close()
    
    return {"networks": networks}


@app.post("/networks/", response_model=NetworkCreate, status_code=status.HTTP_201_CREATED)
def network_create(net: NetworkCreate):
    conn = libvrt.wvmNetworks()
    try:
        conn.create_network(
            net.name,
            net.forward,
            net.gateway,
            net.mask,
            net.dhcp,
            net.bridge,
            net.openvswitch,
            net.fixed
        )
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return net


@app.get("/networks/{name}/", status_code=status.HTTP_200_OK)
def network_info(name):
    try:
        conn = libvrt.wvmNetwork(name)
        network = {
            "name": name,
            "active": conn.get_active(),
            "device": conn.get_bridge_device(),
            "forward": conn.get_ipv4_forward()[0],
        }
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"network": network}


@app.post("/networks/{name}/", response_model=NetworkAction, status_code=status.HTTP_200_OK)
def network_action(name, val: NetworkAction):
    if val.action not in ["start", "stop", "autostart", "manualstart"]:
        raise_error_msg("Action not exist.")

    try:
        conn = libvrt.wvmNetwork(name)

        if val.action == "start":
            conn.start()
        if val.action == "stop":
            conn.stop()
        if val.action == "autostart":
            conn.set_autostart(True)
        if val.action == "manualstart":
            conn.set_autostart(False)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"network": network}


@app.delete("/networks/{name}/")
def network_delete(name):
    try:
        conn = libvrt.wvmNetwork(name)
        conn.stop()
        conn.delete()
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/secrets/", status_code=status.HTTP_200_OK)
def secrets_list():
    secrets_list = []
    conn = libvrt.wvmSecrets()
    for uuid in conn.get_secrets():
        secret = conn.get_secret(uuid)
        secrets_list.append(
            {
                "usage": secret.usageID(),
                "uuid": secret.UUIDString(),
                "usageType": secret.usageType(),
                "value": conn.get_secret_value(uuid),
            }
        )
    conn.close()
    
    return {"secrets": secrets_list}


@app.post("/secrets/", response_model=SecretCreate, status_code=status.HTTP_201_CREATED)
def secret_create(secret: SecretCreate):
    try:
        conn = libvrt.wvmSecrets()
        conn.create_secret(secret.ephemeral, secret.private, secret.secret_type, secret.data)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return secret


@app.get("/secrets/{uuid}/", status_code=status.HTTP_200_OK)
def secret_info(uuid):
    try:
        conn = libvrt.wvmSecrets()
        secret = conn.get_secret(uuid)
        secret = {
            "usage": secret.usageID(),
            "uuid": secret.UUIDString(),
            "usageType": secret.usageType(),
            "value": conn.get_secret_value(uuid),
        }
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"secret": secret}


@app.post("/secrets/{uuid}/", response_model=SecretValue, status_code=status.HTTP_200_OK)
def secret_value(uuid, secret: SecretValue):
    try:
        conn = libvrt.wvmSecrets()
        conn.set_secret_value(uuid, secret.value)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return secret


@app.delete("/secrets/{uuid}/")
def secret_detele(uuid):
    try:
        conn = libvrt.wvmSecrets()
        conn.delete_secret(uuid)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/nwfilters/", status_code=status.HTTP_200_OK)
def nwfilters_list():
    nwfilters_list = []
    try:
        conn = libvrt.wvmNWfilter()
        nwfilters = conn.get_nwfilters()
        for nwfilter in nwfilters:
            nwfilters_list.append({"name": nwfilter, "xml": conn.get_nwfilter_xml(nwfilter)})
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return {"nwfilters": nwfilters_list}


@app.post("/nwfilters/", response_model=NwFilterCreate, status_code=status.HTTP_201_CREATED)
def nwfilter_ctreate(nwfilter: NwFilterCreate):
    try:
        conn = libvrt.wvmNWfilter()
        conn.create_nwfilter(nwfilter.xml)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)
    
    return nwfilter

@app.get("/nwfilters/{name}/", status_code=status.HTTP_200_OK)
def nwfilter_info(name):
    try:
        conn = libvrt.wvmNWfilter()
        nwfilter = {"name": name, "xml": conn.get_nwfilter_xml(name)}
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return {"nwfilter": nwfilter}


@app.delete("/nwfilters/{name}/")
def nwfilter_delete(name):
    try:
        conn = libvrt.wvmNWfilter()
        conn.delete_nwfilter(name)
        conn.close()
    except libvirtError as err:
        raise_error_msg(err)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/floating_ips/", response_model=FloatingIPs, status_code=status.HTTP_200_OK)
def floating_ip_attach(floating_ip: FloatingIPs):
    err_msg = None

    try:
        ip = network.FixedIP(floating_ip.fixed_address)
        err_msg = ip.attach_floating_ip(floating_ip.address, floating_ip.prefix, floating_ip.gateway)
    except Exception as err:
        raise_error_msg(err)

    if err_msg:
        raise_error_msg(err_msg)

    return floating_ip


@app.delete("/floating_ips/", response_model=FloatingIPs)
def floating_ip_detach(floating_ip: FloatingIPs):
    err_msg = None

    try:
        ip = network.FixedIP(floating_ip.fixed_address)
        err_msg = ip.detach_floating_ip(floating_ip.address, floating_ip.prefix)
    except Exception as err:
        raise_error_msg(err)

    if err_msg:
        raise_error_msg(err_msg)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
