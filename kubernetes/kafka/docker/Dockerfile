# kafka version = 3.0.0
# https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc
# get image from strimzi repository
# https://quay.io/repository/strimzi/kafka

FROM quay.io/strimzi/kafka:0.28.0-kafka-3.1.0

# using root user
USER root:root

# create default directory jdbc plugins
RUN mkdir -p /opt/kafka/plugins/kafka-connect-jdbc
RUN mkdir -p /opt/kafka/plugins/kafka-connect-s3

# copy local jars files to image
COPY ./jars/kafka-connect-jdbc/ /opt/kafka/plugins/kafka-connect-jdbc/
COPY ./jars/kafka-connect-s3/ /opt/kafka/plugins/kafka-connect-s3/