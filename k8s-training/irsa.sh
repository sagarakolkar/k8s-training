# Create OIDC Provider
eksctl utils associate-iam-oidc-provider --cluster k8s-training --approve

# Download EKSCTL
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin

# Create Service Account
eksctl create iamserviceaccount \
    --name irsa-test \
    --namespace default \
    --cluster k8s-training \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
    --approve \
    --override-existing-serviceaccounts

# Get Service Account
kubectl get sa irsa-test

# Describe Service Account
kubectl describe sa irsa-test

# Install nginx pod
kubectl apply -f nginx-irsa.yaml

# Install AWS Cli in Pod
apk add --no-cache aws-cli


