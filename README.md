# url-shortener-k8s

A production-style URL shortener built with a microservice architecture, containerized with Docker, and deployed on Kubernetes. The project covers the full stack from REST API design to cloud-native deployment.

## Architecture

```
Client
  │
  ▼
Nginx (reverse proxy, single entry point)
  ├── /auth/*      → Auth Service (Flask, port 5001)
  └── /shortener/* → Shortener Service (Flask, port 5000)
```

Two independent Flask microservices communicate internally. Nginx acts as the single public entry point, routing traffic by path prefix. Each service has its own persistent volume for data storage.

## Skills demonstrated

| Area | Details |
|---|---|
| **REST API design** | Full CRUD endpoints, correct HTTP verbs and status codes |
| **Microservices** | Two decoupled services with internal service discovery |
| **JWT (from scratch)** | HS256 token generation and validation using `hmac` + `base64` — no external JWT library |
| **Authentication flow** | Token-based auth: login → JWT → protected endpoints via `Authorization` header |
| **Docker** | Multi-service `docker-compose.yml`, custom Dockerfiles, named volumes for persistence |
| **Kubernetes** | Deployment manifests, services, persistent volumes, multi-namespace management |
| **Nginx** | Reverse proxy config, path-based routing, header forwarding |
| **Python / Flask** | RESTful routing, JSON request/response handling, environment-based config |

## Services

### Auth Service
Handles user lifecycle and token issuance.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users` | Register a new user |
| `POST` | `/users/login` | Login and receive a JWT |
| `PUT` | `/users/` | Update password |
| `POST` | `/validate` | Validate a JWT (used internally by the shortener) |

### Shortener Service
Manages shortened URLs. All endpoints except `GET /:id` require a valid JWT in the `Authorization` header.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all URLs owned by the authenticated user |
| `GET` | `/:id` | Resolve a short ID to its destination URL |
| `POST` | `/` | Create a new shortened URL |
| `PUT` | `/:id` | Update the destination of an existing short URL |
| `DELETE` | `/:id` | Delete a specific short URL |
| `DELETE` | `/` | Delete all URLs owned by the authenticated user |

## Stack

- **Python 3 / Flask** — microservice logic
- **Nginx** — reverse proxy and single-port exposure
- **Docker & Docker Compose** — containerization and local orchestration
- **Kubernetes** — cluster deployment with `kubectl`
- **JWT / HMAC-SHA256** — stateless authentication

---

## 1) Docker Compose (start, inspect, and stop stack)

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

```bash
# Full details for a specific deployment
kubectl describe deployment <deployment-name> -n <namespace>

# Full details for a specific pod
kubectl describe pod <pod-name> -n <namespace>

# Full details for a specific service
kubectl describe svc <service-name> -n <namespace>
```

## 4) Kubernetes - logs and pod verification

```bash
# Pod logs in current namespace
kubectl logs <pod-name>

# Pod logs in a specific namespace
kubectl -n <namespace> logs <pod-name>

# Extended pod information (including node and IP)
kubectl get pod <pod-name> -o wide
```

## 5) Application endpoint tests with curl

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

```bash
# SSH into the node
ssh <user>@<node-ip>

# List running Docker containers on the node
docker ps

# Restart a specific container
docker restart <container-id>
```

## 7) Kubernetes resource cleanup

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
cat ~/internal-services.yaml
cat ~/nginx.yaml
cat ~/nginx-config.yaml
```
