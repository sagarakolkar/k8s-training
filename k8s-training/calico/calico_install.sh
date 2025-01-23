kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.1/manifests/calico-vxlan.yaml
kubectl -n kube-system set env daemonset/calico-node FELIX_AWSSRCDSTCHECK=Disable