# K8S-RabbitMQ-Autoscaler
An example of autoscaling consumer pods depending on the length of [RabbitMQ](https://www.rabbitmq.com/).
Mainly reference to this [AWS Compute Blog](https://aws.amazon.com/blogs/compute/scaling-kubernetes-deployments-with-amazon-cloudwatch-metrics/), except the metric using for autoscaling is from [Amazon MQ](https://aws.amazon.com/amazon-mq/?amazon-mq.sort-by=item.additionalFields.postDateTime&amazon-mq.sort-order=desc)

# Prerequisites
* kubectl
* a Kubernetes cluster
* a Amazon MQ
* a proper IAM credentials to Kubernetes pods

# Quick Start
1. Replace the **RabbitMQ configs** in the config gile `config.ini`
2. Replace the **image** in the `deploy.yaml`
3. Replace the **broker** in the `external-metric.yaml`
4. (Optional) Build and Push the image
5. Deploy the **k8s-cloudwatch-adapter** with command 
```$ kubectl apply -f https://raw.githubusercontent.com/awslabs/k8s-cloudwatch-adapter/master/deploy/adapter.yaml```
6. Deploy the **consumer** deployment
```$ kubectl apply -f deploy.yaml```
7. Create the **ExternalMetric** reosource
```$ kubectl apply -f external-metric.yaml```
8. Create the [**HPA**](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) resource
```$ kubectl apply -f hpa.yaml```
9. (Optional) **Publish** message to the queue
```python queue.py publish DEFAULT-QUEUUE```


License
----

MIT
