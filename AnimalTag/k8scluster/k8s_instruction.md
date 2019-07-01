# Setting Up a Kubernetes Cluster on AWS

1. [Setting Up K8s on AWS](k8s_instruction.md#setting-up-k8s-on-aws)
2. [Spin Up GPU Enabled K8s](k8s_instruction.md#spin-up-gpu-enabled-k8s)


## Setting Up K8s on AWS
This part is mainly modified from the tutor [here](https://ramhiser.com/post/2018-05-20-setting-up-a-kubernetes-cluster-on-aws-in-5-minutes/)
### Prerequisites: 
* Set up AWS account and AWS CLI
* Install kops + kubectl
* Create an S3 bucket to store the state of K8s cluster and its configuration

### Setting Up K8s
```
$ kops create cluster --node-count=2 --node-size=m4.large --zones=us-east-1a --name zootube.k8s.local
```
This will only generate a cluster configuration, to launch it, run
```
$ kops update cluster --name zootube.k8s.local --yes
```
Waiting a while, validate the cluster to check it is ready to use.
```
$ kops validate cluster
Validating cluster zootube.k8s.local

INSTANCE GROUPS
NAME			ROLE	MACHINETYPE	MIN	MAX	SUBNETS
master-us-east-1a	Master	m4.large	1	1	us-east-1a
nodes			Node	m4.large	2	2	us-east-1a

NODE STATUS
NAME			ROLE	READY
ip-172-20-34-111.ec2.internal	node	True
ip-172-20-40-24.ec2.internal	master	True
ip-172-20-62-139.ec2.internal	node	True
```

To here, the k8s cluster with 1 master node and 2 working nodes are ready to use.

### Update K8s Configuration
Use the following command to change the cluster config, like node `min` `max`, node AIM
```
$ kops edit ig nodes
$ kops edit ig master-us-east-1a
```

Update K8s cluster on AWS with the `Update-Rolling-Validate` procedure.
```
kops update cluster --yes
kops rolling-update cluster
kops validate cluster
```

## Spin Up GPU Enabled K8s

This part is summarized from [**nvidia-device-plugin in kubernetes**](https://github.com/kubernetes/kops/tree/master/hooks/nvidia-device-plugin). No more need to find compatible driver with CUDA toolkit, no install one by one on each node, launched at cluster update.  

### Modify the nodes config to include the nvidia hooks
```
$ kops edit ig nodes
```
add the following blocks
```python
spec:
  image: kope.io/k8s-1.12-debian-stretch-amd64-hvm-ebs-2019-05-13
  machineType: p2.xlarge
  hooks:
  - execContainer:
      image: dcwangmit01/nvidia-device-plugin:0.1.0
```

### Update K8s cluster on AWS with the `Update-Rolling-Validate` procedure.
```
kops update cluster --yes
kops rolling-update cluster
kops validate cluster
```

### Deploy the Daemonset for the Nvidia DevicePlugin
```
$ kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.11/nvidia-device-plugin.yml
```