helm install cilium cilium/cilium \
    --version 1.12.4 \
    --namespace kube-system \
    -f cilium-values.yaml
