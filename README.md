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

[AWS EC2 RHEL Instance Setup — Guide](README/README_RHEL_Setup-Guide.md)

```bash
chmod 400 KeyPair.pem
ssh -i KeyPair.pem ec2-user@54.193.35.129
```

### 5. Install Kubernetes Tools on EC2
 
[Install Kubernetes (kubelet, kubeadm, kubectl) on RHEL — Guide](README/README_Kubernetes_kubelet_kubeadm_kubectl_Install_RHEL.md)


### 6. Create Namespace

```bash
kubectl create namespace production
```

### 7. Deploy Application

**personal_files/deployment.yaml**:
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

**personal_files/service.yaml**:
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
kubectl apply -f personal_files/deployment.yaml
kubectl apply -f personal_files/service.yaml
```

### 8. Verify

```bash
kubectl get pods -n production
kubectl get svc -n production
```

Access your app at:
```
http://54.193.35.129:30007
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
