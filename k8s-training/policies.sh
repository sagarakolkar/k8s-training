kubectl exec -it busybox -- sh
wget -qO- http://nginx-app2.default.svc.cluster.local

kubectl apply -f normal-deny-all-ingress.yaml
kubectl exec -it busybox -- sh
wget -qO- http://nginx-app2.default.svc.cluster.local
