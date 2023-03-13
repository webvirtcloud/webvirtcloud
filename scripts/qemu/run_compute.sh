#!/bin/bash
set -e 

# Check if the .vagrant directory exists
if [ ! -d ".vagrant" ]; then
    mkdir -p .vagrant/webvirtcloud
else
    if [ ! -d ".vagrant/webvirtcloud" ]; then
        mkdir -p .vagrant/webvirtcloud
    fi
fi

# Download the image
if [ ! -f ".vagrant/webvirtcloud/box.img" ]; then
    if [ ! -f "/tmp/rockylinux8.box" ]; then
        wget https://app.vagrantup.com/rockylinux/boxes/8/versions/5.0.0/providers/libvirt.box -O /tmp/rockylinux8.box        
    fi
    tar -zxf /tmp/rockylinux8.box -C .vagrant/webvirtcloud
    qemu-img resize .vagrant/webvirtcloud/box.img +256G
fi

case "$1" in
    start) sudo qemu-system-x86_64 \
           -accel tcg \
           -smp 6 \
           -m 8192 \
           -drive if=virtio,file=.vagrant/webvirtcloud/box.img \
           -device e1000,netdev=qemu0 -netdev vmnet-shared,id=qemu0 \
           -device e1000,netdev=mgmt0 -netdev vmnet-shared,id=mgmt0 \
           -device e1000,netdev=publ0 -netdev vmnet-shared,id=publ0 \
           -device e1000,netdev=priv0 -netdev vmnet-shared,id=priv0 \
           -display none -daemonize
        ;;
    kill) sudo kill -9 `ps ax | grep "qemu-system-x86_64" | awk 'NR==1{print $1}'`
        ;;
    *) echo "Usage: (start|kill)"
esac

# Add subnets to bridge interface
sudo ifconfig bridge100 alias 172.64.0.1 255.255.255.0
sudo ifconfig bridge100 alias 192.168.33.1 255.255.255.0
sudo ifconfig bridge100 alias 10.132.0.1 255.255.255.0

exit 0