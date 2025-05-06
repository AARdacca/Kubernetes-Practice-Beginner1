# Module 6 Assignment: Dockerize, Push to Docker Hub & Deploy on Kubernetes (AWS EC2)

This project documents the process of Dockerizing a Django application, pushing it to Docker Hub, and deploying it on a Kubernetes cluster hosted on an AWS EC2 instance.

## Repository

- GitHub: [RapidCompetitions](https://github.com/roy35-909/RapidCompetitions)

---

## Docker Hub Image

- Repository: [aliahasan/ostad-mastering_devops_batch001-module06](https://hub.docker.com/r/aliahasan/ostad-mastering_devops_batch001-module06)
- Tag: `rapidcomp_app-v1`

---

## Folder Structure

```
<working-dir>/
├── .env
├── Dockerfile
├── deployment.yaml
├── service.yaml
└── RapidCompetitions/
    └── (Django project files)
```

> All operations are run from `<working-dir>`. No `cd RapidCompetitions` is used.

---

## Steps

### 1. Clone the Repository

```bash
git clone https://github.com/roy35-909/RapidCompetitions.git
```

### 2. Dockerize the Application

**Dockerfile** is placed in `<working-dir>`:

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY RapidCompetitions/requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential zlib1g-dev libffi-dev libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Django project and .env file
COPY RapidCompetitions /app
COPY .env /app/.env

# Set environment variable file for Django (if you use django-environ or similar)
ENV DJANGO_READ_DOT_ENV_FILE=true

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 3. Build & Push Docker Image

```bash
# from <working‑dir>
docker build -t rapidcomp_local:test .
docker run -p 8000:8000 rapidcomp_local:test
# open http://localhost:8000 to confirm it works
docker stop $(docker ps -q --filter ancestor=rapidcomp_local:test)

docker tag rapidcomp_local:test \
           aliahasan/ostad-mastering_devops_batch001-module06:rapidcomp_app-v1

docker login      
# enter Docker Hub creds if not already logged in
docker push aliahasan/ostad-mastering_devops_batch001-module06:rapidcomp_app-v1
```

### 4. Launch EC2 Instance

```bash
chmod 400 Pair_key_01.pem
ssh -i Pair_key_01.pem ubuntu@52.53.175.164
```

### 5. Install Kubernetes Tools on EC2

```bash
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable --now docker

# Install kubeadm, kubelet, kubectl
sudo apt install -y apt-transport-https ca-certificates curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update && sudo apt install -y kubelet kubeadm kubectl
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

### 6. Create Namespace

```bash
kubectl create namespace production
```

### 7. Deploy Application

**deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rapidcomp-deployment
  namespace: production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rapidcomp
  template:
    metadata:
      labels:
        app: rapidcomp
    spec:
      containers:
      - name: rapidcomp
        image: aliahasan/ostad-mastering_devops_batch001-module06:rapidcomp_app-v1
        ports:
        - containerPort: 8000
```

**service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: rapidcomp-service
  namespace: production
spec:
  type: NodePort
  selector:
    app: rapidcomp
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30007
```

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 8. Verify

```bash
kubectl get pods -n production
kubectl get svc -n production
```

Access your app at:
```
http://52.53.175.164:30007
```

---

## Submission Checklist

- [x] Dockerfile placed outside project directory
- [x] Docker image pushed to Docker Hub
- [x] Kubernetes manifests created in root
- [x] Application deployed in production namespace
- [x] Access verified via NodePort

---

## Author

- **Docker Hub:** aliahasan
- **GitHub:** roy35-909
