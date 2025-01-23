kubectl patch daemonset aws-node -n kube-system --patch "$(cat aws-node-patch.yaml)"
