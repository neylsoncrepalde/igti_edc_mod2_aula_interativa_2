```sh
# access working directory
cd kubernetes/kafka

# add helm chart
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# create namespace
kubectl create namespace kafka

# install helm strimzi-operator
helm install kafka strimzi/strimzi-kafka-operator --namespace kafka --version 0.28.0
kubectl get pods -n kafka -w

# expected output
NAME                                    READY   STATUS    RESTARTS   AGE
strimzi-cluster-operator-6d48cd-7pzm6   0/1     Running   0          38s
strimzi-cluster-operator-6d48cd-7pzm6   1/1     Running   0          41s

# deploy mode jbod
kubectl apply -f deployments/broker/kafka-jbod.yaml -n kafka

# terminal
$ kafka.kafka.strimzi.io/edh created

# get pods
kubectl get pods -n kafka

# expected output after a few seconds
NAME                                    READY   STATUS    RESTARTS   AGE
edh-kafka-0                             1/1     Running   0          58s
edh-kafka-1                             1/1     Running   0          58s
edh-kafka-2                             1/1     Running   0          58s
edh-zookeeper-0                         1/1     Running   0          2m3s
edh-zookeeper-1                         1/1     Running   0          2m3s
edh-zookeeper-2                         1/1     Running   0          2m3s
strimzi-cluster-operator-6d48cd-7pzm6   1/1     Running   0          5m19s

# create secret for mssql and s3
kubectl create secret generic mssql-credentials --from-file=deployments/connect/mssql-credentials.properties --namespace kafka
kubectl create secret generic aws-s3-credentials --from-file=deployments/connect/aws-s3-credentials.properties --namespace kafka

# terminal
$ secret/mssql-credentials created
$ secret/aws-s3-credentials created

# describe on secrets
kubectl describe secret mssql-credentials -n kafka

# expected output
Name:         mssql-credentials
Namespace:    kafka
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
mssql-credentials.properties:  46 bytes

# describe on secrets
kubectl describe secret aws-s3-credentials -n kafka

# expected output
Name:         aws-s3-credentials
Namespace:    kafka
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
aws-s3-credentials.properties:  103 bytes

# create image kafka-connect
docker build .\
          -t <username>/kafka-connect-strimzi:0.28.0-kafka-3.1.0 \
          -f docker/Dockerfile

docker push <username>/kafka-connect-strimzi:0.28.0-kafka-3.1.0

# deploy kafka-connect
kubectl apply -f deployments/connect/kafka-connect.yaml -n kafka

# terminal
$ kafkaconnect.kafka.strimzi.io/kafka-class created

# expected ouput after a few seconds
NAME                                            READY   STATUS    RESTARTS   AGE
kafka-class-connect-69d6885b68-g8pxw            1/1     Running   0          4m2s
kafka-class-kafka-0                             1/1     Running   0          11m
kafka-class-kafka-1                             1/1     Running   0          11m
kafka-class-kafka-2                             1/1     Running   0          11m
kafka-class-zookeeper-0                         1/1     Running   0          12m
kafka-class-zookeeper-1                         1/1     Running   0          12m
kafka-class-zookeeper-2                         1/1     Running   0          12m
strimzi-cluster-operator-6d48cd-7pzm6           1/1     Running   0          15m

# check kafkaconnect
kubectl get kafkaconnect -n kafka

# expected output
NAME           DESIRED REPLICAS   READY
kafka-class    1                  True

# create connectors 
kubectl apply -f manifests/source/src-mssql-products.yaml -n kafka
kubectl apply -f manifests/source/src-mssql-users.yaml -n kafka
kubectl apply -f manifests/source/src-mssql-sales.yaml -n kafka

$ kafkaconnector.kafka.strimzi.io/ingest-src-mssql-products created
$ kafkaconnector.kafka.strimzi.io/ingest-src-mssql-users created
$ kafkaconnector.kafka.strimzi.io/ingest-src-mssql-sales created

# check connectors
kubectl get kafkaconnectors -n kafka

# expected output
NAME                        CLUSTER       CONNECTOR CLASS                                 MAX TASKS   READY
ingest-src-mssql-products   kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True
ingest-src-mssql-sales      kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True
ingest-src-mssql-users      kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True

# see topic
kubectl -n kafka exec kafka-class-kafka-0 -c kafka -it -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# expected output
__consumer_offsets
connect-cluster-configs
connect-cluster-offsets
connect-cluster-status
mssql-products
mssql-sales
mssql-users

# get data on topic with group consumer
kubectl exec kafka-class-kafka-0 -n kafka -c kafka -it -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --property print.key=true \
    --topic mssql-sales \
    --group MyConsumer

# get all data on topic
kubectl exec kafka-class-kafka-0 -n kafka -c kafka -it -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --property print.key=true \
    --from-beginning \
    --topic mssql-sales

# expected json data
{"schema":{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1},"payload":1660591709250}        {"schema":{"type":"struct","fields":[{"type":"int32","optional":false,"field":"userid"},{"type":"int32","optional":false,"field":"productid"},{"type":"int32","optional":true,"field":"quantity"},{"type":"string","optional":true,"field":"price"},{"type":"int32","optional":true,"field":"paymentmtd"},{"type":"int32","optional":true,"field":"paymentsts"},{"type":"string","optional":true,"field":"dt_insert"},{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"dt_update"},{"type":"string","optional":true,"field":"messagetopic"},{"type":"string","optional":true,"field":"messagesource"}],"optional":false},"payload":{"userid":1,"productid":1,"quantity":5,"price":"$2,565.32","paymentmtd":1,"paymentsts":3,"dt_insert":"2022-08-15 19:28:29.250","dt_update":1660591709250,"messagetopic":"mssql-sales","messagesource":"sqlserver"}}
{"schema":{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1},"payload":1660591709250}        {"schema":{"type":"struct","fields":[{"type":"int32","optional":false,"field":"userid"},{"type":"int32","optional":false,"field":"productid"},{"type":"int32","optional":true,"field":"quantity"},{"type":"string","optional":true,"field":"price"},{"type":"int32","optional":true,"field":"paymentmtd"},{"type":"int32","optional":true,"field":"paymentsts"},{"type":"string","optional":true,"field":"dt_insert"},{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"dt_update"},{"type":"string","optional":true,"field":"messagetopic"},{"type":"string","optional":true,"field":"messagesource"}],"optional":false},"payload":{"userid":17,"productid":9,"quantity":9,"price":"$1,059.56","paymentmtd":1,"paymentsts":3,"dt_insert":"2022-08-15 19:28:29.250","dt_update":1660591709250,"messagetopic":"mssql-sales","messagesource":"sqlserver"}}

# create sink to storage data on datalake s3
kubectl apply -f manifests/sink/sink-s3-products.yaml -n kafka
kubectl apply -f manifests/sink/sink-s3-users.yaml -n kafka
kubectl apply -f manifests/sink/sink-s3-sales.yaml -n kafka

# terminal
$ kubectl get kafkaconnectors -n kafka

# expected output
NAME                        CLUSTER       CONNECTOR CLASS                                 MAX TASKS   READY
ingest-src-mssql-products   kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True
ingest-src-mssql-sales      kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True
ingest-src-mssql-users      kafka-class   io.confluent.connect.jdbc.JdbcSourceConnector   1           True
sink-s3-products            kafka-class   io.confluent.connect.s3.S3SinkConnector         1           True
sink-s3-sales               kafka-class   io.confluent.connect.s3.S3SinkConnector         1           True
sink-s3-users               kafka-class   io.confluent.connect.s3.S3SinkConnector         1           True
```