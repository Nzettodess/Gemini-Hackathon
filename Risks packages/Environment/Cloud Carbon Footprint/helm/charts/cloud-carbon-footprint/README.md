<!--- app-name:  cloud-carbon-footprint -->

# Helm Chart for Cloud Carbon Foot Print

Cloud Carbon Footprint is an application that estimates the energy (kilowatt hours) and carbon emissions (metric tons CO2e) of public cloud provider utilization.


## TL;DR

```console
git clone https://github.com/appnetwise/cloud-carbon-footprint.git
cd helm/charts/cloud-carbon-footprint
helm install cloud-carbon-footprint .
```

## Introduction

[Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org) is an application that estimates the energy (kilowatt hours) and carbon emissions (metric tons CO2e) of public cloud provider utilization.

If you would like to learn more about the various calculations and constants that we use for the emissions estimates, check out the [Methodology page](https://www.cloudcarbonfootprint.org/docs/methodology)



## Prerequisites

- Kubernetes
- Helm 

## Installing the Chart

To install the chart with the release name `my-release`:

```console
helm install my-release .
```

## Parameters
### Client Configuration

| Parameter                                   | Description                                                                            | Default Value                                                                            |
|---------------------------------------------|----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| `client.configmap.resolver`                 | Resolver configuration for the client                                                  | `""`                                                                                     |
| `client.deployment.replicaCount`            | Number of replicas for the client deployment                                           | `2`                                                                                      |
| `client.deployment.image.repository`        | Docker image repository for the client                                                 | `docker.io/cloudcarbonfootprint/client`                                                  |
| `client.deployment.image.tag`               | Docker image tag for the client                                                        | `release-2024-02-11` |
| `client.deployment.image.pullPolicy`        | Image pull policy for the client                                                       | `IfNotPresent`                                                                           |
| `client.deployment.imagePullSecrets`        | Secrets for pulling the client image                                                   | `[]`                                                                                     |
| `client.deployment.securityContext`         | Security context for the client deployment                                             | See below for details                                                                    |
| `client.deployment.resources`               | Resource requests and limits for the client                                            | `{}`                                                                                     |
| `client.deployment.affinity`                | Affinity settings for the client deployment                                            | `[]`                                                                                     |
| `client.deployment.tolerations`             | Tolerations for the client deployment                                                  | `[]`                                                                                     |
| `client.deployment.topologySpreadConstraints`| Topology spread constraints for the client deployment                                  | `[]`                                                                                     |
| `client.serviceAccount.annotations`         | Annotations for the client service account                                             | `{}`                                                                                     |
| `client.service.type`                       | Type of service for the client                                                         | `ClusterIP`                                                                              |
| `client.service.port.name`                  | Name of the client service port                                                        | `http`                                                                                   |
| `client.service.port.number`                | Port number for the client service                                                     | `80`                                                                                     |
| `client.ingress.enabled`                    | Enable ingress for the client                                                          | `false`                                                                                  |
| `client.ingress.className`                  | Ingress class name for the client                                                      | `''`                                                                                     |
| `client.ingress.hosts`                      | Hostnames for the client ingress                                                       | `[{ host: cloud-carbon-footprint.example.com }]`                                         |
| `client.ingress.tls`                        | TLS configuration for the client ingress                                               | `[]`                                                                                     |
| `client.pdb.enabled`                        | Enable Pod Disruption Budget for the client                                            | `true`                                                                                   |
| `client.pdb.minAvailable`                   | Minimum number of available client pods                                                | `1`                                                                                      |

#### Security Context for Client

| Parameter                           | Description                                                | Default Value                          |
|-------------------------------------|------------------------------------------------------------|----------------------------------------|
| `client.deployment.securityContext.capabilities.add`    | Capabilities to add                                        | `[CHOWN, SETGID, SETUID]`              |
| `client.deployment.securityContext.capabilities.drop`   | Capabilities to drop                                       | `[ALL]`                                |

### API Configuration

| Parameter                                | Description                                                                             | Default Value                                                                            |
|------------------------------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| `api.configmap`                          | Configuration map for the API                                                           | `{}`                                                                                     |
| `api.deployment.replicaCount`            | Number of replicas for the API deployment                                               | `2`                                                                                      |
| `api.deployment.image.repository`        | Docker image repository for the API                                                     | `docker.io/cloudcarbonfootprint/api`                                                     |
| `api.deployment.image.tag`               | Docker image tag for the API                                                            | `release-2024-02-11` |
| `api.deployment.image.pullPolicy`        | Image pull policy for the API                                                           | `IfNotPresent`                                                                           |
| `api.deployment.imagePullSecrets`        | Secrets for pulling the API image                                                       | `[]`                                                                                     |
| `api.deployment.securityContext`         | Security context for the API deployment                                                 | See below for details                                                                    |
| `api.deployment.resources`               | Resource requests and limits for the API                                                | `{}`                                                                                     |
| `api.deployment.affinity`                | Affinity settings for the API deployment                                                | `[]`                                                                                     |
| `api.deployment.toleration`              | Tolerations for the API deployment                                                      | `[]`                                                                                     |
| `api.deployment.topologySpreadConstraints`| Topology spread constraints for the API deployment                                      | `[]`                                                                                     |
| `api.serviceAccount.annotations`         | Annotations for the API service account                                                 | `{}`                                                                                     |
| `api.service.type`                       | Type of service for the API                                                             | `ClusterIP`                                                                              |
| `api.service.port.name`                  | Name of the API service port                                                            | `http`                                                                                   |
| `api.service.port.number`                | Port number for the API service                                                         | `80`                                                                                     |
| `api.pdb.enabled`                        | Enable Pod Disruption Budget for the API                                                | `true`                                                                                   |
| `api.pdb.minAvailable`                   | Minimum number of available API pods                                                    | `1`                                                                                      |

#### Security Context for API

| Parameter                           | Description                                                | Default Value                          |
|-------------------------------------|------------------------------------------------------------|----------------------------------------|
| `api.deployment.securityContext.capabilities.drop`   | Capabilities to drop                                       | `[ALL]`                                |

## Usage

To deploy the CloudCarbonFootprint application using this Helm chart, you can use the following command:

```sh
helm install cloud-carbon-footprint ./cloud-carbon-footprint -f values.yaml
```

You can override the default values by specifying them in the `values.yaml` file or by using the `--set` flag when running the `helm install` command.

For example, to set the `client.deployment.replicaCount` to 3 and enable the client ingress, you can use the following command:

```sh
helm install cloud-carbon-footprint ./cloud-carbon-footprint --set client.deployment.replicaCount=3 --set client.ingress.enabled=true
```

## Additional Information

For more information about the CloudCarbonFootprint project, please visit the [GitHub repository](https://github.com/appnetwise/cloud-carbon-footprint).

---
