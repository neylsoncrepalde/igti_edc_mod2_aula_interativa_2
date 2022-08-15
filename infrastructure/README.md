## Deployment the Stack with *eksctl*
```sh
cd infrastructure

# Change cluster name on "deploy_eks.sh" file
sh deploy_eks.sh

# access cluster
kubectl get nodes

# expected output
NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-0-2-101.us-east-2.compute.internal   Ready    <none>   24s   v1.20.11-eks-f17b81
ip-10-0-2-42.us-east-2.compute.internal    Ready    <none>   24s   v1.20.11-eks-f17b81
ip-10-0-3-104.us-east-2.compute.internal   Ready    <none>   23s   v1.20.11-eks-f17b81
ip-10-0-3-198.us-east-2.compute.internal   Ready    <none>   24s   v1.20.11-eks-f17b81

# After implementing the exercise, delete the cluster
sh delete_eks.sh
```