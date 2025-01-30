# No Policies
kubectl exec -it busybox -- sh
wget -qO- http://nginx-app2.default.svc.cluster.local

# Block all ingress
kubectl apply -f normal-deny-all-ingress.yaml
kubectl exec -it busybox -- sh
wget -qO- http://nginx-app2.default.svc.cluster.local

# Allow ingress from same namespace
normal-all-busybox-ingress.yaml
kubectl exec -it busybox -- sh

# Allow ingress from pods in same namespace with specific label
kubectl apply -f normal-busybox-with-nginx-label.yaml 
kubectl exec -it busybox -- sh
kubectl apply -f busybox-nginx.yaml
kubectl exec -it busybox-nginx -- sh
