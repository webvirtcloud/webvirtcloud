# WebVirtCloud #

WebVirtCloud is a web-based virtualization platform that allows users to manage and create virtual machines on a remote server. It uses git submodules to build the backend and frontend components of the platform.

## KVM node Configuration ##

[WebVirtCompute](https://github.com/webvirtcloud/webvirtcompute) is small daemon which allows to manage virtual machines on the node via WebVirtCloud. It is written in Python and uses libvirt and libvirt-python. WebVirtCompute is a part of WebVirtCloud and is located in the `webvirtcloud/webvirtcompute` directory. Check README.md for more information.


## Configuration Backend and Frontend (BETA) ##

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
git submodule init
git submodule update
```

4. Build the Docker image:
```bash
docker compose build
```

5. Run the Docker container with the production settings (ENV):
```bash
docker compose -f docker-compose.yml -f production.yml up -d
```

6. Run the database migrations:
```bash
docker compose exec backend python3 manage.py migrate
```

7. Load the initial data:
```bash
docker compose exec backend python3 manage.py loaddata initial_data
```

## License ##

WebVirtCloud is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.
