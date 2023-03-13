import os
import paramiko
from subprocess import call, STDOUT, DEVNULL

from settings import BACKUP_USER, BACKUP_KEY_FILE
from .util import md5sum
from .libvrt import wvmConnect
from .libguestfs import GuestFSUtil


ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))


class Backup(object):
    def __init__(self, backup_image_path, image_path):
        self.backup_image_path = backup_image_path
        self.image_path = image_path

    def transfer(self, node):
        """
        usage:
            backup_path_from = path_from + '/' + backup
            backup_path_to = path_to + '/' + backup
            b = Backup(backup_path_from, backup_path_to)
            b.transfer("192.168.1.20")
        :param node:
        :return:
        """
        backup_key_file = os.path.join(ROOT_DIR, BACKUP_KEY_FILE)
        backup_path_from = self.backup_image_path
        backup_path_to = self.image_path
        err_msg = None

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(node, username=BACKUP_USER, key_filename=backup_key_file)
            sftp = ssh.open_sftp()
            sftp.put(backup_path_from, backup_path_to)
            sftp.close()
        except Exception as err:
            err_msg = err

        return err_msg

    def restore(self, disk_size, distro, image_md5sum):
        backup_image_md5 = None
        err_msg = None

        try:
            backup_image_md5 = md5sum(self.backup_image_path)
        except IOError as err:
            err_msg = f"Check image MD5: {str(err)}"

        if backup_image_md5:
            if image_md5sum == backup_image_md5:
                err_msg = self._prepare_image(disk_size, distro, True)
            else:
                err_msg = "MD5 sum mismatch"

        return err_msg

    def deploy(self, template_name, template_md5sum, networks, cloud, public_key, hostname, root_password, disk_size):
        err_msg = "MD5 sum mismatch"
        backup_image_md5 = None

        try:
            backup_image_md5 = md5sum(self.backup_image_path)
        except IOError:
            pass

        if template_md5sum == backup_image_md5:
            err_msg = self._prepare_image(disk_size, template_name)
            if not err_msg:
                try:
                    # Load GuestFS
                    gstfish = GuestFSUtil(self.image_path, template_name)
                    gstfish.mount_root()
                    gstfish.setup_networking(networks, cloud=cloud)
                    gstfish.set_pubic_keys(public_key)
                    gstfish.set_hostname(hostname)
                    gstfish.reset_root_passwd(root_password)
                    gstfish.clean_cloud_init()
                    gstfish.clearfix()
                    gstfish.close()
                except RuntimeError as err:
                    err_msg = err

        return err_msg

    def _prepare_image(self, disk_size, distro, clearfix=False):
        err_msg = None
        resize_disk = False
        conn = wvmConnect()
        backup_image_libvirt = conn.get_volume_by_path(self.backup_image_path)
        if backup_image_libvirt.info()[1] < disk_size:
            qemu_img_cmd = f"qemu-img convert -f qcow2 -O raw {self.backup_image_path} {self.image_path}"
            run_qemu_img_cmd = call(qemu_img_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_qemu_img_cmd == 0:
                image_libvirt = conn.get_volume_by_path(self.image_path)
                image_libvirt.resize(disk_size)
                resize_disk = True
            else:
                err_msg = "Error convert snapshot to image"
        else:
            qemu_img_cmd = f"qemu-img convert -f qcow2 -O raw {self.backup_image_path} {self.image_path}"
            run_qemu_img_cmd = call(qemu_img_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_qemu_img_cmd != 0:
                err_msg = "Error convert snapshot to image"
        conn.close()

        if resize_disk:
            try:
                # Load GuestFS
                gstfish = GuestFSUtil(self.image_path, distro)
                gstfish.resize_fs()
                gstfish.clearfix(firstboot=False)
                gstfish.close()
            except RuntimeError as err:
                err_msg = err

        return err_msg

    def create(self):
        image_md5 = None
        image_size = None
        disk_size = None
        err_msg = None

        # Full image backup path
        if os.path.isdir(os.path.dirname(self.backup_image_path)):
            qemu_img_cmd = f"qemu-img convert -c -f raw -O qcow2 {self.image_path} {self.backup_image_path}"
            run_qemu_img_cmd = call(qemu_img_cmd.split(), stdout=DEVNULL, stderr=STDOUT)
            if run_qemu_img_cmd == 0:
                conn = wvmConnect()
                image_libvirt = conn.get_volume_by_path(self.image_path)
                disk_size = image_libvirt.info()[1]
                image_size = image_libvirt.info()[2]
                conn.close()

                image_md5 = md5sum(self.backup_image_path)
            else:
                err_msg = "Error convert image to snapshot"
        else:
            err_msg = "Snapshot path does not exist"

        return err_msg, image_md5, image_size, disk_size
