kubectl exec -it eks-sample-linux-deployment-6c4c887655-8q2px -n app1 -- sh
kubectl exec -it eks-sample-linux-deployment-6c4c887655-8q2px -n app2 -- sh
  
curl -ivk eks-sample-nginx-service2.app2.svc.cluster.local
curl -ivk eks-sample-nginx-service.app1.svc.cluster.local  
