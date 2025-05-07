# RHEL EC2 Instance Setup (t3.medium)

This guide outlines the steps to set up a **Red Hat Enterprise Linux (RHEL)** EC2 instance of type **t3.medium**, including necessary security group configurations.

## 💥 EC2 Instance Configuration

* **Instance Type:** t3.medium
* **Operating System:** Red Hat Enterprise Linux (RHEL)
* **Region:** \[Specify your AWS Region]
* **Key Pair:** \[Your key pair file, e.g., `MyKey.pem`]
* **Storage:** Minimum 20 GB (recommended)

---

## 🔐 Security Group Rules

### 1. All TCP (for testing or development only)

* **ID:** sgr-0b1e728e0520ce3a8
* **Protocol:** TCP
* **Port Range:** 0 – 65535
* **Source:** 0.0.0.0/0

> ⚠️ *Use with caution — this opens all TCP ports to the world.*

### 2. SSH Access

* **ID:** sgr-00dbf365a332f1118
* **Protocol:** TCP
* **Port Range:** 22
* **Source:** 0.0.0.0/0

> ✅ *Used for remote access to the EC2 instance via SSH.*

### 3. HTTP Access

* **ID:** sgr-04440763d0589db22
* **Protocol:** TCP
* **Port Range:** 80
* **Source:** 0.0.0.0/0

> ✅ *Used for web server hosting or serving applications.*

### 4. HTTPS Access

* **ID:** sgr-03919b93c08c70baf
* **Protocol:** TCP
* **Port Range:** 443
* **Source:** 0.0.0.0/0

> ✅ *Used for secure HTTPS communication.*

---

## 🔧 Basic Setup Commands

### 1. SSH into the instance

```bash
chmod 400 MyKey.pem
ssh -i MyKey.pem ec2-user@<EC2_PUBLIC_IP>
```

### 2. Update system packages

```bash
sudo yum update -y
```

### 3. Install essential packages

```bash
sudo yum install -y git curl wget vim unzip
```

---

## 📌 Recommendations

* **Disable All TCP Access (0-65535)** for production environments.
* Use **Security Group Tags** to organize access by function (SSH, HTTP, etc.).
* Regularly **rotate your key pairs** and review open ports.

---

## ✅ Next Steps

* Set up your application or tools (Docker, Kubernetes, etc.)
* Configure firewalls, monitoring, and backups.
* Consider setting up **CloudWatch** for monitoring or **IAM roles** for EC2.
