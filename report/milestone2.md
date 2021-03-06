
# CSC792 Linux Networking milestone 2

Anran Zhou(azhou6@ncsu.edu) && Zecao Lu(zlu24@ncsu.edu)

## 1) Project Description

We choose the load balancing as a service as our project topic.

Load balancing is a technology that has been around for some time and is a foundation for delivering highly available resources over a network.

At a high level, load balancing is typically accomplished by having a load balancer or set of load balancers present a virtual server to a set of clients. This virtual server is backed by a pool of “real” servers that provide some type of resource to those clients. The role of the load balancer is to distribute client requests across the pool of servers including rerouting requests when a member of the pool fails. Clients are not aware which “real” server in the pool are servicing their requests since they are only aware of the virtual server presented by the load balancer.

Load balancers were implemented by hardware devices in the past. With the advent of the cloud, we can see virtual load balancers are used to provide services to a pool of virtual servers. The function of virtual load balancers and physical load balancers are the same. But there are two major benefits of using virtual load balancers. The first is allowing users to provision load balancers on demand and in the case of metered clouds. The second is allowing users to pay for load balancing services on a utility basis.

In this project, we plan to make VMs on the same or different Linux physical machines act as virtual load balancers to distribute loads on multiple target servers. These load balancers are VM migrated and can be configured automatically.

## 2) Related Work

We investigated two popular products in the market. One is AWS Elastic Load Balancing. The other is Google Cloud Load Balancing.

### 2a) AWS Elastic Load Balancing

There are three types of Load balancers provided by AWS which are **Application Load Balancer**, **Network Load Balancer** and **Classic Load Balancer**.

  

There are some common features among these three load balancer, like: **High Availability**, **Health checks**, **Performance Monitoring**, **Logging** and **Cross-zone load balancing**. The representative unique features of each Load balancer are summarized as follows:

| Load balancer | Unique Features |
|:--------:|:-------------:|
| Application | Layer-7 Load Balancing, Content-Based Routing, More Security Options|
| Network | High Throughput, Low Latency, Static and Elastic IP address |

So the customers can select the appropriate load balancers based on their application needs. If they need flexible application management, they can use an Application Load Balancer. If extreme performance and static IP is needed for their application, they can use a Network Load Balancer. If they have an existing application that was built within the EC2-Classic network, they can use a Classic Load Balancer.

  

### 2b) Google Cloud Load Balancing

Google Cloud Load Balancing provides 5 different load balancers. We can divide those five load balancers by three aspects: Area(Global/Regional), Scope(External/Internal) and Traffic Type. The following table provides some specifics about each load balancer:

| Load balancer | Traffic type |Global/Regional |External/Internal |
|:--------:|:-------------:|:-------------:|:-------------:|
| HTTP(S) | HTTP or HTTPS |Global |External |right-aligned |
| SSL Proxy | TCP with SSL offload |Global |External |
| TCP Proxy | TCP without SSL offload. Does not preserve client IP addresses|Global |External |
| Network TCP/UDP | TCP/UDP without SSL offload. Preserves client IP addresses. |Regional |External |
| Internal TCP/UDP | TCP or UDP |Regional |Internal |

The features of google load balancers are summarized as below:

* Provide HTTP(S), TCP/SSL, UDP Load Balancing.

* Advanced Features. Such as IPv6 Global Load Balancing, WebSockets, user-defined request headers, and protocol forwarding for private VIPs.

* Stack driver Logging logs all the load balancing requests to debug and analyze user traffics.

* Autoscaling handles increases in traffic and reduces cost when the need for resources is lower.

* Health Checks ensure that new connections are only load balanced to healthy backends that are up and ready to receive them.

* Cloud CDN Integration improves the performance.

  

### 2c) Comparison

AWS load balancers and Google Cloud Load Balancer both provide the feature of high availability, automatic scaling, internal load balancing, global load balancing and robust security, etc. But there are still some differences listed in the table below.

| feature | AWS |Google |comments
|:--------:|:-------------:|:-------------:|:-------------:|
|load balancers types| 3 different LBs | 5 different LBs | Google provides LBs with more detailed classification.
|platform|AWS VPC | Google cloud| they both need their own platform to use load balancing feature.
|supported protocols|HTTP(s), TCP, SSL|HTTP(S), TCP/SSL, UDP and proxy| Google support more protocols when applying LB |
|CDN|no use| Google cloud CDN| Google combined CDN with LB to improve performance.

## 3) Feature Implementation
The architecture is like the graph below:

![](./architecture.png)

### 3a) Functional Feature
There are mainly four features of our LBaaS. 
-  HTTP level load balancing
-  Health checker

The Interfaces of key components in this architecture are listed below using Python:
* Controller
	```Python
	class Controller:
	    def __init__(self):
	        """
			"""
	        self.projects = {}
	    
	    def add_project(self, user: string, project: Project):
	        """ add a new project
			Parameters:
			user: user 
			project: project to be added
			"""
	        if self.projects.has_key(user):
	            self.projects[user].append(project)
	        else:
	            self.proejcts[user] = [project]
	    
	    def remove_project(self, user, project: Project):
	        """ remove a project
			"""

	    def update_info_all(self):
	        """ update all projects status
			"""

	    def update_info(self, project: Project):
	        """ read collected log to update the status
			"""
	```
* Project
	```Python
	class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.subnet = Subnet()
        self.vms = []

    def init_subnet(self):
        """ create and initializa a network namespace
		"""
        self.subnet.initialize()
    
    def add_vm(self, vm: VM):
        """ attach a new VM in the current project
		"""
        self.subnet.add_vm(vm)
        self.vms.append(vm)

    def remove_vm(self, vm: VM):
        """ remove a VM from the current project
		"""
        self.subnet.remove_vm(vm)
        self.vms.remove(vm)
	```
* Subnet
	```Python
	class Subnet:
    def __init__(self):
        self.name = ""
        self.id = -1

    def initializa(self):
        """ create a new network namespace
		"""

    def add_vm(self, vm: VM):
        """ create a new L2 bridge and attach to the namespace
		"""

    def remove_vm(self, vm: VM):
        """ detach and destroy corresponding bridge
		"""
	```
* VM
	```Python
	class VM:
	    def __init__(self):
	        self.id = -1

	    def create(self):
	        """ create a new VM
			"""

	    def delete(self):
	        """ delete it
			"""

	    def initializa(self):
	        """ install packets, collected and configure
			"""
	    
	    def add_backend(self, ip: string):
	        """ add a backend server
			"""
	    
	    def remove_backend(self, ip: string):
	        """ remove a backend server
			"""
	    
	    def update_backend(self, old_ip: string, new_ip: string):
	        """ update a bacend server
			"""
	    
	    def attach_to_subnet(self):
	        """ attack to subnet
			"""
	```

When a user create a new project, there are the following steps:
1.  Controller create a VM and get an IP
2.  Configure LB functions on that VM
3.  Health checker machine register that new VM
4.  Register VM ip on DNS and get the URL
5.  If this is a new project, Create a new namespace(subnet).
6.  Return the URL to users

We can realize health checker using collectd framework and we plan to design data structures to store the monitor logs.

### 3b) management feature

#### Availability & Reliability
To make sure the health status of our instances, we deployed the health checker function in our controller. Basically it receive the user-defined parameters of interval, timeout and retries. For virtual machine, we used collectd framework to collect the real-time status of each virtual machine. And for docker container, we implemented this function based on docker inspect command. 

The logic for two secereny are the same. The health check will first run interval seconds and then again interval seconds after each previous check completes. If a single run of the check takes longer than timeout seconds then the check is considered to have failed. It takes retries consecutive failures of the health check for the container to be considered unhealthy.

#### 3. User Interface & Configurability
We provide two methods for users to do the configuration and control their VPCs. One is CLI written in Python, the other one is the web app.

* CLI interfaces
This interface is realized by calling a python script. Users can define the JSON formatted configuration files and then send them to the controller. Then the returned value are displayed on the terminal.

Here are some templates of user's input:
```json
{
    "action": ["create"/"info"/"update"/"delete"],
    "type": ["project"/"instance"],
    "info": {
        "name": "example"
    }
}
```
The template of returned value:
```json
{
    "status": ["successful"/"fail"],
    "action": "create",
    "type": "project",
    "info": {
        "name": "example",
        "id": 1,
    }
}
```
For project, instance and subnets, we have more specific configurations:
* Project
	```json
	{
	    "type": "project",
	    "user": "john",
	    "name": "john's project",
	    "instances": [],
	}
	```

* Instance
	```json
	{
	    "type": "instance",
	    "traffic_type": ["tcp"/"http"],
	    "subnet": "1.1.1.0/24",
	    "backend": {
	        "entities": [
	            ["ip"/"url"], ...
	        ],
	        "health-check": {},
	        "auto-scaling": true,
	    }
	}
	```

* health check
	check the status of backend servers:
	```json
	{
	    "protocol": ["HTTP"/"TCP"],
	    "port": 80,
	    "request-path": "/",
	    "criteria": {
	        "interval": 5,
	        "timeout": 5,
	        "health-threshold": 2,
	        "unhealth-threshold": 2
	    }
	}
	```
	
## Architecture

![alt text](./northbound.png)

### View Layer

The view layer is responsible for parsing the JSON request and dispatch the command to the corresponding models.

### Model Layer

In Django framework, a model is the single, definitive source of information about the data. It contains the essential fields and behaviors of the data. In our project, we have three models: project, subnet and instance. There is no difference between virtual machine implementation and docker container since we put the infrastructure dependent code in the utility functions.

![alt text](./er.png)

The project model stores user name and project name, it could manipulate the project namespace. The subnet model stores ip address of the subnet and a project foreigh key because the project table and subnet are one-to-many relationship. It could manipulate the subnet bridge. And instance model stores the backends ip and health check parameters. It is responsible for manipulating the instance(virtual machine). 


### Utility functions

The utility file defines some common used functions and execution logic of ansible scripts. The functions in model actually call the helper functions in utility to execute ansible scripts.

### Health Checker

For the virtual machine, we used the libvirt plugin of collectd framework to collect the real-time running status of each virtual machine. We checked the instances every interval seconds. After getting the status, controller could return it to the user as a real-time info request. And put it into the health check functions. That is, if  there are retries consecutive failures of the health check, the instance will be considered unhealthy.

### Ansible
We have five kinds of ansible scripts. 
#### Namespace
For creating namespace, we used ip command to created a new namespace, and attch it to the admin namespace using a veth pair. Then changed ip route to add default routing to the new veth pair, finally did a iptables SNAT operation.

For deleting namespace, just shut down the related devices such as veth pairs then deleted them.

#### L2 net
For creating a new L2 network, we used virsh tool to define a new network based on template and used a veth pair to attach it to the project namespace.

For deleteing the bridge, just make down it and then delete it using brctl.

#### Instance
For creating a new virtual machine, we cloned a new one from our template virtual machine. Then used virsh attach-interface to attach to the bridge. Then changed routing table using ip route to make the default interface be the new one.

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTc0OTY2ODMxNiwxMjk5MzEyODk2LDE3MT
ExNTc5NTIsLTE5OTQ3NjgxOTgsMTM4NTIwNTAwNiwtMTg4NDg4
Njc0NywtMTQwODUzOTc5LDE2NDE1OTYyNDUsNzMwOTk4MTE2XX
0=
-->