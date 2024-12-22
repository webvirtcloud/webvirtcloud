# WebVirtCloud Milti-Region Network Topology (Beta)

## Network Scheme

```text
                     [ Internet ] ----------------------+
                          |                             |
                          |                             |
                +---------------------+                 |
                |                     |                 |
                |    WebVirtCloud     |                 |
                |     Controller      |                 |
                |                     |                 |
                +---------------------+                 |
                           |                            |
                    [ VPN Network ]                     |
                           |                            |
                +---------------------+                 |
                |                     |                 |
                |    Region Gateway   | ----------------+
                |      "New York"     |                 |
                |                     |                 |
                +---------------------+                 |
                  |                ||                   |
    [ Management Network ]   [ Pivate Network ]         |
                  |                ||                   |
                  +----------------------+              |
                  |                ||    |              |
             +======================+    |              |
             ||   |                ||    |              |
             ||   |                ||    |              |
   +---------------------+  +---------------------+     |
   |                     |  |                     |     |
   |      Compute 1      |  |      Compute 2      |     |
   |                     |  |                     |     |
   | [ Compute Network ] |  | [ Compute Network ] |     |
   |                     |  |                     |     |
   +---------------------+  +---------------------+     |
                |                     |                 |
                +---------------------+                 |
                          |                             |
                  [ Public Network ] -------------------+
```

## Network Interfaces

### Gateway interfaces

The gateway has three network interfaces:

- **Managenent Network**
- **Private Network**
- **Public Network**

The gateway is used to route traffic between the controller and the compute nodes. Gateway must have two physical network interfaces or one physical network interface with VLANs.

### Compute Interfaces

Each compute nodes have three network interfaces:

- **Management Network** 
- **Private Network**
- **Public Network**

It can be one physical network interface with VLANs or multiple physical network interfaces.

## Network Description

### VPN Network

The VPN network is used to connect the controller to the gateway. This network provides access from controller to management and private networks.

### Management Network

The management network is used to connect the controller to compute nodes. This network is used to manage the compute nodes and the virtual machines running on them.

### Compute Network

The compute network is used to connect the compute virtual machines to the compute node. This network configured inside compute and used to for feature like Floating IP.

### Private Network

The private network is used to connect the compute nodes for the virtual machines. This network provides access to virtual machines for manage services running on them like Load Balancer, Database, K8s, etc.

### Public Network

The public network is used to connect the virtual machines to the internet.
