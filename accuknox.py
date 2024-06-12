
1 The Project involves containerizing the application, deploying it on kubernates, setting up CI/CD 
pipelines with github actions, and securing it with TLS.

1 Dokerization
To containerize wisecow application, create a Dockerfile in the root of your repository. 
Dockerfie
# use an official Python runtime as a parent image
FROM python:3.9-slim
# set the working directory in the container
WORKDIR /app
# Copy the current directory contains into the contaner at app
COPY . / app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# make port 80 available to the world outside this container 
EXPOSE 80
# Define environment variable
ENV NAME Wisecow
# Run app.py when the container launches
CMD ["PYTHON","APP.PY]
2.Kubernetes Deployment
Create the Kubernetes manifest files to deploy the Wisecow application.
Deployment Manifest (`deployment.yaml`)yaml
apiVersion: apps/v1
kind: Deployment

metadata:
 name: wisecow-deployment
spec:
 replicas: 3
 selector:
 matchLabels:
 app: wisecow
 template:
 metadata:
 labels:
 app: wisecow
 spec:
 containers:
 - name: wisecow
 image: your-docker-repo/wisecow:latest
 ports:
 - containerPort: 80
```
## Service Manifest (`service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
 name: wisecow-service
spec:
 selector:
 app: wisecow
 ports:
 - protocol: TCP
 port: 80
 targetPort: 80
 type: LoadBalancer
```
3. Continuous Integration and Deployment (CI/CD)
Set up GitHub Actions to automate building and pushing the Docker image, and deploying it to 
Kubernetes.
GitHub Actions Workflow (`.github/workflows/ci-cd.yml`)
```yaml
name: CI/CD Pipeline
on:
 push:
 branches:
 - main
jobs:
 build:
 runs-on: ubuntu-latest
steps:
 - name: Checkout code
 uses: actions/checkout@v2
 - name: Set up kubectl
 uses: azure/setup-kubectl@v1
 with:
 version: 'latest'
 - name: Set up Kubeconfig
 run: |
 echo "${{ secrets.KUBE_CONFIG }}" > $HOME/.kube/config
 - name: Deploy to Kubernetes
 run: |
 kubectl apply -f deployment.yaml
 kubectl apply -f service.yaml
```
4. TLS Implementation
To secure the application with TLS, you can use cert-manager to automatically provision TLS certificates 
from Let's Encrypt.
Install cert-manager
sh
kubectl apply -f
https://github.com/jetstack/cert-manager/releases/download/v1.6.1/cert-manager.yaml
Issuer Manifest (`issuer.yaml`)
yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
 name: letsencrypt-prod
spec:
 acme:
 server: https://acme-v02.api.letsencrypt.org/directory
 email: your-email@example.com
 privateKeySecretRef:
 name: letsencrypt-prod
 solvers:
 - http01:
 ingress:
 class: nginx
Ingress Manifest (`ingress.yaml`)
yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
 name: wisecow-ingress
 annotations:
 cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
 rules:
 - host: yourdomain.com
 http:
 paths:
 - path: /
 pathType: Prefix
 backend:
 service:
 name: wisecow-service
 port:
 number: 80
 tls:
 - hosts:
 - yourdomain.com
 secretName: wisecow-tls
```
Summary of Expected Artifacts
-Dockerfile: To build the Docker image.
Kubernetes manifests: Deployment (`deployment.yaml`), Service (`service.yaml`), Issuer (`issuer.yaml`), 
and Ingress (`ingress.yaml`) files.
GitHub Actions workflow: `.github/workflows/ci-cd.yml`.
Access Control
Make sure the GitHub repository is set to public, and the necessary secrets (like `DOCKER_USERNAME`, 
`DOCKER_PASSWORD`, and `KUBE_CONFIG`) are added to the repository's secrets.
By following these steps, you'll containerize the Wisecow application, deploy it to a Kubernetes 
environment, automate the CI/CD process, and secure it with TLS communication.
2 Let's tackle two objectives from the list:
1. System Health Monitoring Script
2. Log File Analyzer
I'll provide scripts for both tasks in Python.
1. System Health Monitoring Script
This Python script will monitor CPU usage, memory usage, disk space, and running processes. If any 
metric exceeds predefined thresholds, it will log an alert.
python
import psutil
import logging
from datetime import datetime
# Set thresholds
CPU_THRESHOLD = 80 # in percent
MEMORY_THRESHOLD = 80 # in percent
DISK_THRESHOLD = 80 # in percent
# Setup logging
logging.basicConfig(filename='system_health.log', level=logging.INFO,
 format='%(asctime)s - %(levelname)s - %(message)s')
def log_alert(message):
 logging.warning(message)
 print(message)
def check_cpu():
 cpu_usage = psutil.cpu_percent(interval=1)
 if cpu_usage > CPU_THRESHOLD:
 log_alert(f"High CPU usage detected: {cpu_usage}%")
 else:
 print(f"CPU usage is normal: {cpu_usage}%")
def check_memory():
 memory = psutil.virtual_memory()
 memory_usage = memory.percent
 if memory_usage > MEMORY_THRESHOLD:
 log_alert(f"High Memory usage detected: {memory_usage}%")
 else:
 print(f"Memory usage is normal: {memory_usage}%

def check_disk():
 disk = psutil.disk_usage('/')
 disk_usage = disk.percent
 if disk_usage > DISK_THRESHOLD:
 log_alert(f"High Disk usage detected: {disk_usage}%")
 else:
 print(f"Disk usage is normal: {disk_usage}%")
def check_processes():
 processes = [(proc.info['name'], proc.info['cpu_percent']) for proc in psutil.process_iter(['name', 
'cpu_percent'])]
 for proc in processes:
 if proc[1] > CPU_THRESHOLD:
 log_alert(f"High CPU usage by process {proc[0]}: {proc[1]}%")
def main():
 check_cpu()
 check_memory()
 check_disk()
 check_processes()
if __name__ == "__main__":
 main()
2. Log File Analyzer
This Python script will analyze a web server log file to find the number of 404 errors, the most requested 
pages, and the IP addresses with the most requests.
python
import re
from collections import Counter
# Path to the log file
LOG_FILE = 'access.log'
def parse_log_line(line):
 # Example log line: '127.0.0.1 - - [10/Jun/2024:12:34:56 +0000] "GET /index.html HTTP/1.1" 200 
1024'
 match = re.match(r'(\S+) - - \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)', line)
 if match:
 return {
 'ip': match.group(1),
 'datetime': match.group(2),
 'method': match.group(3),
 'url': match.group(4),
 'protocol': match.group(5),
 'status': int(match.group(6)),
 'size': int(match.group(7))
}
 return None
def analyze_log_file(log_file):
 with open(log_file, 'r') as file:
 logs = [parse_log_line(line) for line in file if parse_log_line(line)]
 # Count 404 errors
 errors_404 = [log for log in logs if log['status'] == 404]
 num_404_errors = len(errors_404)
 # Most requested pages
 requested_pages = [log['url'] for log in logs]
 most_requested_pages = Counter(requested_pages).most_common(10)
 # IP addresses with most requests
 ip_addresses = [log['ip'] for log in logs]
 most_frequent_ips = Counter(ip_addresses).most_common(10)
 # Output the summary report
 print(f"Number of 404 errors: {num_404_errors}")
 print("\nTop 10 requested pages:")
 for page, count in most_requested_pages:
 print(f"{page}: {count} requests")
 
 print("\nTop 10 IP addresses with most requests:")
 for ip, count in most_frequent_ips:
print(f"{ip}: {count} requests")
def main():
 analyze_log_file(LOG_FILE)
if __name__ == "__main__":
 main()
These scripts can be further customized based on specific needs and extended to include additional functionality.

