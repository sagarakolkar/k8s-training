kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.1/manifests/calico-vxlan.yaml
kubectl -n kube-system set env daemonset/calico-node FELIX_AWSSRCDSTCHECK=Disable
curl -L https://github.com/projectcalico/calico/releases/download/v3.29.1/calicoctl-linux-amd64 -o calicoctl
chmod +x calicoctl
