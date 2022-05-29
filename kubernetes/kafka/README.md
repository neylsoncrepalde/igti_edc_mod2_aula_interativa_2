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

# create connectors ingest-src-mssql-vehicle-json-0bf03203
kubectl apply -f manifests/source/src-mssql-vehicle.yaml -n kafka

$ kafkaconnector.kafka.strimzi.io/ingest-src-mssql-vehicle-json-0bf03203 created

# check connectors
kubectl get kafkaconnectors -n kafka

# expected output
NAME                                     CLUSTER   CONNECTOR CLASS                                 MAX TASKS   READY
ingest-src-mssql-vehicle-json-0bf03203   edh       io.confluent.connect.jdbc.JdbcSourceConnector   1           True

# see topic
kubectl -n kafka exec kafka-class-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# expected output
__consumer_offsets
connect-cluster-configs
connect-cluster-offsets
connect-cluster-status
src-mssql-vehicle

# get data on topic with group consumer
kubectl exec kafka-class-kafka-0 -n kafka -c kafka -i -t -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --property print.key=true \
    --topic src-mssql-vehicle \
    --group MyConsumer

# get all data on topic
kubectl exec kafka-class-kafka-0 -n kafka -c kafka -i -t -- \
  bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --property print.key=true \
    --from-beginning \
    --topic src-mssql-vehicle

# expected json data
   "schema":{
      "type":"int32",
      "optional":false
   },
   "payload":1
}{
   "schema":{
      "type":"struct",
      "fields":[
         {
            "type":"int32",
            "optional":false,
            "field":"id"
         },
         {
            "type":"int32",
            "optional":false,
            "field":"customer_id"
         },
         {
            "type":"string",
            "optional":true,
            "field":"ano_modelo"
         },
         {
            "type":"string",
            "optional":true,
            "field":"modelo"
         },
         {
            "type":"string",
            "optional":true,
            "field":"fabricante"
         },
         {
            "type":"string",
            "optional":true,
            "field":"ano_veiculo"
         },
         {
            "type":"string",
            "optional":true,
            "field":"categoria"
         },
         {
            "type":"string",
            "optional":true,
            "field":"messagetopic"
         },
         {
            "type":"string",
            "optional":true,
            "field":"messagesource"
         }
      ],
      "optional":false
   },
   "payload":{
      "id":1,
      "customer_id":0,
      "ano_modelo":"2022",
      "modelo":"Uno",
      "fabricante":"Fiat",
      "ano_veiculo":"2022",
      "categoria":"Hatch",
      "messagetopic":"src-mssql-vehicle",
      "messagesource":"sqlserver"
   }
}

# create sink to storage data on datalake s3
kubectl apply -f manifests/sink/sink-s3-vehicle.yaml -n kafka

# terminal
$ kubectl get kafkaconnectors -n kafka

# expected output
NAME                                     CLUSTER   CONNECTOR CLASS                                 MAX TASKS   READY
ingest-src-mssql-vehicle-json-0bf03203   edh       io.confluent.connect.jdbc.JdbcSourceConnector   1           True
sink-s3-vehicle-json-0bf03203            edh       io.confluent.connect.s3.S3SinkConnector         1           True
```