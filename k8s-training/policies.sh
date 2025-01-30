# No Policies
kubectl exec -it busybox -- sh
wget -qO- http://nginx-app2.default.svc.cluster.local

# Block all ingress
kubectl apply -f normal-deny-all-ingress.yaml
kubectl get NetworkPolicy
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


# Download calicoctl
curl -L https://github.com/projectcalico/calico/releases/download/v3.29.1/calicoctl-linux-amd64 -o calicoctl
chmod +x ./calicoctl

#Apply calico global policy 
./calicoctl apply -f calico-global-policy.yaml
./calicoctl get GlobalNetworkPolicy

kubectl exec -it busybox-nginx -- sh
wget -qO- http://nginx-app1.app1.svc.cluster.local

#Apply calico global policy - allow few ns
kubectl label namespace default allowed-
kubectl apply -f calico-global-allow-few-ns.yaml
./calicoctl get GlobalNetworkPolicy

kubectl exec -it busybox-nginx -- sh
wget -qO- http://nginx-app1.app1.svc.cluster.local

kubectl label namespace default allowed=nginx
kubectl exec -it busybox-nginx -- sh
wget -qO- http://nginx-app1.app1.svc.cluster.local
