kubectl create ns advanced-policy-demo
kubectl create deployment --namespace=advanced-policy-demo nginx --image=nginx
kubectl expose --namespace=advanced-policy-demo deployment nginx --port=80
kubectl run --namespace=advanced-policy-demo access --rm -ti --image busybox /bin/sh
