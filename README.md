# WebVirtCloud #

WebVirtCloud is a web-based virtualization platform that allows users to manage and create virtual machines on a remote server. It uses git submodules to build the backend and frontend components of the platform.

## Controller configuration (BETA) ##

To install WebVirtCloud, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/webvirtcloud/webvirtcloud.git
```

2. Change into the webvirtcloud directory:

```bash
cd webvirtcloud
```

3. Run script for deploy WebVirtCloud:

```bash
./webvirtcloud.sh env
```

4. Start WebVirtCloud:

```bash
./webvirtcloud.sh start
```

6. Open client side in browser (example for domain: `webvirt.local`):

```url
http://client.webvirt.local
```

7. Open admin side in browser (example for domain: `webvirt.local`):

```url
http://manage.webvirt.local
```

If you use `webvirt.local` wildcard domain you need to allow SSL certificate in browser (optional):

```url
https://assets.webvirt.local
```

## Update controller ##

Run script for update:

```bash
./webvirtcloud.sh update
```

## Compute configuration ##

More information about the hypervisor configuration can be found in the [WebVirtCompute](https://github.com/webvirtcloud/webvirtcompute) repository.

## License ##

WebVirtCloud is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.
