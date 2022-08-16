# Processamento em tempo real com Spark Structured Streaming

```sh
# Create the namespace
kubectl create namespace spark

# Create service account
kubectl create serviceaccount spark -n spark

# Create Cluster Role binding
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=spark:spark --namespace=spark

# Create secret with AWS credentials
kubectl create secret -n spark generic aws-credentials \
--from-literal=aws_access_key_id=<AWS_ACCESS_KEY_ID> \
--from-literal=aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>

# Add helm chart and install it on Kubernetes
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo update
helm install spark spark-operator/spark-operator --namespace spark
helm ls -n spark

# File from_kafka_to_delta.py should be on Amazon S3. Then, deploy the streaming process:
cd processing
kubectl apply -f from_kafka_to_delta.yaml -n spark

# Get pods' status
kubectl get pods -n spark

# Get spark application status
kubectl get sparkapplication -n spark

# Follow spark application logs
kubectl logs -f job-pyspark-streaming-users-aggregated-driver -n spark 
```