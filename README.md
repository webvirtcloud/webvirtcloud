# WebVirtCloud #

WebVirtCloud is a web-based virtualization platform that allows users to manage and create virtual machines on a remote server. It uses git submodules to build the backend and frontend components of the platform.

## Backend and Frontend configuration (BETA) ##

To install WebVirtCloud, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/webvirtcloud/webvirtcloud.git
```

2. Change into the webvirtcloud directory:


```bash
cd webvirtcloud
```

3. Initialize and update the submodules:

```bash
git submodule init webvirtbackend
git submodule init webvirtfrontend
git submodule update
```

4. Build the Docker image:
```bash
docker compose build
```

5. Run the Docker container with the production settings (ENV):

 Create file `custom.env` add the next variables with your domain records:

```text
BASE_DOMAIN=webvirt.local
API_DOMAIN=api.webvirt.local
ASSETS_DOMAIN=assets.webvirt.local
CLIENT_DOMAIN=client.webvirt.local
MANAGE_DOMAIN=manage.webvirt.local
CONSOLE_DOMAIN=console.webvirt.local
```

Run docker compose:

```bash
docker compose up -d
```

6. Run the database migrations:
```bash
docker compose exec backend python3 manage.py migrate
```

7. Load the initial data:
```bash
docker compose exec backend python3 manage.py loaddata initial_data
```

## Hypervisor configuration ##

More information about the hypervisor configuration can be found in the [WebVirtCompute](https://github.com/webvirtcloud/webvirtcompute) repository.

## License ##

WebVirtCloud is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.