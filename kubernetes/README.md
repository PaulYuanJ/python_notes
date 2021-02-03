# 在Centos7上安装Kubernetes集群

## 在Centos7上安装Docker

```
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# yum install docker-ce
```

## 在所有节点安装工具
```
# yum install -y kubelet kubeadm kubectl
# systemctl enable kubelet 
```

## 在master节点拉取镜像
```
# kubeadm config images pull --image-repository registry.aliyuncs.com/google_containers 
```

## 初始化master节点
```
# kubeadm init --kubernetes-version=v1.20.2 --pod-network-cidr=10.31.0.0/16 --apiserver-advertise-address=192.168.56.103 --image-repository registry.aliyuncs.com/google_containers
# mkdir -p $HOME/.kube
# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# sudo chown $(id -u):$(id -g) $HOME/.kube/config
# export KUBECONFIG=/etc/kubernetes/admin.conf
```

## 在其他的工作节点执行命令，使接入集群, 请根据实际情况替换参数中的所有token和
```
# kubeadm join 192.168.56.103:6443 --token 5uut43.ktn8luxztoqg2jcr discovery-token-ca-cert-hash sha256:9ea8dde3ef369c0447d579e0fed67e763b5758bf028eeda19a940c7e094f7792 
```

## 在master节点安装calico网络
```
# kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

## 检查集群中所有节点的label
```
# kubectl get nodes --show-labels
```

## 将工作节点的role改了worker
```bash
# kubectl label nodes node01 node-role.kubernetes.io/worker=
# kubectl label nodes node02 node-role.kubernetes.io/worker=
```

# 安装监控系统

## 在master节点执行命令以安装监控系统
```
# git clone https://github.com/prometheus-operator/kube-prometheus.git
# cd kube-prometheus
# kubectl apply -f manifests/setup
# kubectl apply -f manifests/
```
注意：如果要对外使用NodePort暴露服务，在manifests目录下找到相关service的yaml进行配置即可。安装监控系统的目的是为了让集群内跑起来一套可用的系统，这样我们在调用api的时候，好知道具体的情况。

# 安装kubernetes相关python模块

## 使用pip命令安装模块kubernetes
```
# pip install Kubernetes -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
注：这个模块给出的api对于普通运维来说命名有些晦涩，无法和我们常用的kubectl命令结合起来，为了方便，我这里将里面的一些方法进行了二次封装，更符合普通运维使用。见KubeClient.py
