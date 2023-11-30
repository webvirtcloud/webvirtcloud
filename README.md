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

3. Initialize and update the submodules:

```bash
git submodule init webvirtbackend webvirtfrontend
git submodule update
```

4. Run the Docker container with the production settings (ENV):

Create file `custom.env` add the next variables with your domain records. 

Example `custom.env` for domain `webvirt.local`:

```text
BASE_DOMAIN=webvirt.local
API_DOMAIN=api.webvirt.local
ASSETS_DOMAIN=assets.webvirt.local
CLIENT_DOMAIN=client.webvirt.local
MANAGE_DOMAIN=manage.webvirt.local
CONSOLE_DOMAIN=console.webvirt.local
```

Check the `global.env` file for more information about the variables.

5. Build the Docker image:
```bash
docker compose build
```

* If you want to use controller on your local machine you can use domain `webvirt.local` and you need add the next line to `/etc/hosts` file.

```text
127.0.0.1 api.webvirt.local client.webvirt.local manage.webvirt.local assets.webvirt.local console.webvirt.local
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

8. Open the Admin WebVirtCloud interface in your browser:

```url
http://admin.webvirt.local
```

9. Open the Client WebVirtCloud interface in your browser:

```url
http://client.webvirt.local
```

## Update controller ##

To update WebVirtCloud, follow these steps:

1. Stop the Docker container:

```bash
docker compose down
```

2. Pull the latest changes from the repository:

```bash
git pull
```

3. Update the submodules:

```bash
git submodule update
```

4. Build the Docker image:

```bash
docker compose build --no-cache
```

5. Run the Docker container:

```bash
docker compose up -d
```

6. Run the database migrations:

```bash
docker compose exec backend python3 manage.py migrate
```

## Compute configuration ##

More information about the hypervisor configuration can be found in the [WebVirtCompute](https://github.com/webvirtcloud/webvirtcompute) repository.

## License ##

WebVirtCloud is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.
