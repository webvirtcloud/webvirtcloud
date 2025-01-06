<p align="center">
  <img src="https://cloud-assets.webvirt.cloud/images/github-preview.png">
</p>

# WebVirtCloud

**WebVirtCloud** is a web platform for managing virtual machines (VMs) on remote servers. It offers an alternative to platforms like DigitalOcean, Linode, and Vultr, allowing users to host and control their virtual machines independently.

## Features

- **User Management:** Create and manage user accounts.
- **VM Management:** Create, manage, and delete virtual machines on remote servers.
- **VM Templates:** Pre-configured templates for Ubuntu, Debian, Fedora, CentOS, AlmaLinux, and Rocky Linux.
- **Firewall Management:** Configure firewall rules for virtual machines.
- **Floating IP Management:** Assign and manage floating IP addresses.
- **Load Balancer:** Set up and manage load balancers to distribute traffic across virtual machines.

## Architecture

WebVirtCloud consists of two main components:
- **Controller:** A web interface to manage virtual machines.
- **Compute Node:** A hypervisor that runs the virtual machines.

It is recommended to install the Controller and Compute Node on separate servers.

## Requirements

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installing the Controller

To install WebVirtCloud, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/webvirtcloud/webvirtcloud.git
cd webvirtcloud
```

2. Set up Caddy:

    To configure TLS for the web server, copy either the `Caddyfile.selfsigned` or `Caddyfile.letsencrypt` and without TLS `Caddyfile.noncert` template to `Caddyfile`. 

    > **NOTE**: Caddy does not support TLS for bare IP addresses. If you need TLS, you can use a domain name with a service like [nip.io](https://nip.io) as a workaround.

    For example, if your IP address is 192.168.0.114, you can use `192-168-0-114.nip.io` as your domain name. Below, we demonstrate how to set up a self-signed certificate for the domain `webvirtcloud-192-168-0-114.nip.io`:

- For TLS with self-signed certificates:

```bash
mkdir -p .caddy/certs
openssl req -x509 -newkey rsa:4096 -keyout .caddy/certs/key.pem -out .caddy/certs/cert.pem -days 365 -nodes -subj "/CN=webvirtcloud-192-168-0-114.nip.io"
cp Caddyfile.selfsigned Caddyfile
```

- Without TLS:

```bash
cp Caddyfile.noncert Caddyfile
```

3. Run the setup script:

```bash
./webvirtcloud.sh env
```

Example:

```bash
Enter your domain or IP address (only HTTP). Default: localhost
Enter: webvirtcloud-192-168-0-114.nip.io
```

4. Start WebVirtCloud:

```bash
./webvirtcloud.sh start
```

For first-time users, refer to the [Features](#features) section to explore the capabilities of WebVirtCloud.

## Accessing the Interface

- **User Panel:** [https://webvirtcloud-192-168-0-114.nip.io](https://webvirtcloud-192-168-0-114.nip.io)
- **Admin Panel:** [https://webvirtcloud-192-168-0-114.nip.io/admin/](https://webvirtcloud-192-168-0-114.nip.io/admin/)

Ensure your firewall allows access to ports 80 (HTTP) and 443 (HTTPS) for the WebVirtCloud interface.

## Default Credentials

- **Username:** `admin@webvirt.cloud`
- **Password:** `admin`

> **Warning:** It is critical to change the default credentials immediately after the first login to ensure security.

## Update the Controller

To update the controller, run:

```bash
./webvirtcloud.sh update
```

If new features or templates are added:

```bash
./webvirtcloud.sh loaddata
```

## Additional Settings

The `env.local` file is used to store environment variables. You can edit this file to define your environment-specific configurations. Ensure environment variables are formatted consistently, as shown below:

```bash
# Email environment variables
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=admin
EMAIL_HOST_PASSWORD=admin
EMAIL_USE_TLS=True
EMAIL_FROM="WebVirtCloud <noreply@gmail.com>"
```

## Installing the Compute Node (Hypervisor)

See the [WebVirtCompute](https://github.com/webvirtcloud/webvirtcompute) repository for detailed instructions.

> **Warning:** After updating the controller, make sure to update the [WebVirtCompute daemon](https://github.com/webvirtcloud/webvirtcompute?tab=readme-ov-file#update-webvirtcompute-daemon) on all compute nodes to ensure compatibility.

## Private networking

If your server does not have additional network interfaces for a private network, you can use [WireGuard](https://www.wireguard.com) VPN to establish a private connection between the controller and the compute node.

> **Important:** The Load Balancer feature requires access to the private network from the controller to deploy and manage HAProxy on a virtual machine.

## License

WebVirtCloud is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.
