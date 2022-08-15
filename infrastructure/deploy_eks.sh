eksctl create cluster \
    --managed --alb-ingress-access --node-private-networking --full-ecr-access --asg-access \ # fixed definitions
    --name=kubea3dataney \
    --instance-types=m6i.xlarge \
    --region=us-east-1 \
    --nodes-min=2 --nodes-max=3 \
    --nodegroup-name=ng-kubea3dataney
