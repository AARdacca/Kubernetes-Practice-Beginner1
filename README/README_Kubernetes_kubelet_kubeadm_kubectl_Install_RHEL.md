# Kubernetes Single-Node Cluster Setup on RHEL EC2 Instance

This guide will walk you through installing and configuring Docker, Kubernetes (kubeadm, kubectl, kubelet), and initializing a single-node Kubernetes cluster on a RHEL-based EC2 instance.

---

## Step 1: Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<EC2_PUBLIC_IP>
```

---

## Step 2: Install Docker

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker
```

---

## Step 3: Configure containerd for Kubernetes

```bash
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
```

Edit the config file:

```bash
sudo nano /etc/containerd/config.toml
```

Find and modify:

```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
```

Restart containerd:

```bash
sudo systemctl restart containerd
sudo systemctl status containerd
```

---

## Step 4: Add Kubernetes Repository & Install Tools

```bash
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
EOF

sudo yum install -y kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
```

---

## Step 5: Disable Swap

```bash
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab
```

---

## Step 6: Initialize Kubernetes Cluster

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

Save the `kubeadm join` command for later use (for adding nodes).

---

## Step 7: Set Up kubectl for ec2-user

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

## Step 8: Install Network Add-on (Calico)

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml
```

---

## Step 9: Verify Everything Works

```bash
kubectl get nodes -o wide
kubectl get pods --all-namespaces
```

If `STATUS` is `Ready`, your single-node Kubernetes cluster is up and running.

---

## Troubleshooting

* Ensure containerd is running: `sudo systemctl status containerd`
* Use `journalctl -u kubelet -xe` for kubelet errors
* Restart Docker or containerd if changes made

---

> **Note:** This guide is optimized for RHEL 8/9-based EC2 instances and Kubernetes v1.32
