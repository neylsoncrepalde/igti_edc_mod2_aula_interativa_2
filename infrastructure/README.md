## Deployment the Stack with Terraform :terraform:
```sh
cd infrastructure/aws

# init terraform
terraform init

# see the execution plan
terraform plan

# apply the configs
terraform apply

# variables environment
aws eks list-clusters --region us-east-1
# output
<CLUSTER_NAME>

# update kubeconfig context
aws eks --region us-east-1 update-kubeconfig --name <CLUSTER_NAME>

# access cluster
kubectl get nodes

# expected output
NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-2-101.us-east-2.compute.internal   Ready    <none>   24s   v1.20.11-eks-f17b81
ip-10-0-2-42.us-east-2.compute.internal    Ready    <none>   24s   v1.20.11-eks-f17b81
ip-10-0-3-104.us-east-2.compute.internal   Ready    <none>   23s   v1.20.11-eks-f17b81
ip-10-0-3-198.us-east-2.compute.internal   Ready    <none>   24s   v1.20.11-eks-f17b81
```