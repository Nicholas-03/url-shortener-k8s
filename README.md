# URL Shortener — Docker, Kubernetes & Endpoint Reference

## 1) Docker Compose (start, inspect, and stop stack)
These commands manage the containers defined in `docker-compose.yml`.

```bash
# Start all services in the background and build images
docker compose -f docker-compose.yml up --build -d

# Show stack container status
docker compose -f docker-compose.yml ps

# Stream logs in real time
docker compose -f docker-compose.yml logs -f

# Stop and remove stack containers
docker compose -f docker-compose.yml down
```

## 2) Kubernetes - deployment and cluster status
This group applies manifests and checks the overall status of the cluster and resources.

```bash
# Verify the Kubernetes cluster is reachable
kubectl cluster-info

# Apply all YAML manifests in the current folder
kubectl apply -f .

# List cluster nodes
kubectl get nodes

# List pods in the current namespace
kubectl get pods

# List pods across all namespaces
kubectl get -A pods

# List deployments across all namespaces
kubectl get deployments -A

# List services across all namespaces
kubectl get svc -A

# List endpoints across all namespaces
kubectl get endpoints -A

# List pods across all namespaces with extra details (node IP, etc.)
kubectl get pods -A -o wide

# Periodically refresh node view
watch kubectl get nodes

# Periodically refresh pod view across all namespaces
watch kubectl get -A pods
```

## 3) Kubernetes - detailed resource diagnostics
Use `describe` to inspect events, configuration, errors, and internal state of deployments/pods/services.

```bash
# Full details for a specific deployment
kubectl describe deployment <deployment-name> -n <namespace>

# Full details for a specific pod
kubectl describe pod <pod-name> -n <namespace>

# Full details for a specific service
kubectl describe svc <service-name> -n <namespace>
```

## 4) Kubernetes - logs and pod verification
Quick commands to read application logs and check where a pod is running.

```bash
# Pod logs in current namespace
kubectl logs <pod-name>

# Pod logs in a specific namespace
kubectl -n <namespace> logs <pod-name>

# Extended pod information (including node and IP)
kubectl get pod <pod-name> -o wide
```

## 5) Application endpoint tests with curl
These tests verify app reachability and responses via NodePort, public domain, or Host header (useful with Ingress/reverse proxy).

```bash
# Test root endpoint via NodePort
curl http://<node-ip>:<nodeport>/

# Test shortener endpoint via NodePort
curl http://<node-ip>:<nodeport>/shortener/0

# Test root endpoint via public domain
curl http://app.nicholasboidi.tech/

# Test shortener endpoint via public domain
curl http://app.nicholasboidi.tech/shortener/0

# Test with Host header forced to the VM public IP
curl -H "Host: app.nicholasboidi.tech" http://<public-vm-ip>/shortener/0
```

## 6) Node access and local container management
This group is useful for troubleshooting directly on the node machine.

```bash
# SSH into the node
ssh <user>@<node-ip>

# List running Docker containers on the node
docker ps

# Restart a specific container
docker restart <container-id>
```

## 7) Kubernetes resource cleanup
Remove all resources defined by manifests applied from the current directory.

```bash
# Delete resources created from YAML files in the current folder
kubectl delete -f .
```

## 8) Files and manifests reference

### Docker Compose stack
- `docker-compose.yml`
- `default.conf`
- `Dockerfile` (auth microservice)
- `Dockerfile` (shortener microservice)

### Kubernetes manifests
- `internal-services.yaml`
- `nginx.yaml`
- `nginx-config.yaml`

### VM files generated during cluster setup
- `~/.kube/config`
- `/etc/kubernetes/admin.conf`
- `/var/lib/kubelet/config.yaml`
- `/var/lib/kubelet/kubeadm-flags.env`

### Read manifest files on the VM
```bash
# Show internal services manifest
cat ~/internal-services.yaml

# Show nginx deployment/service manifest
cat ~/nginx.yaml

# Show nginx config map manifest
cat ~/nginx-config.yaml
```
