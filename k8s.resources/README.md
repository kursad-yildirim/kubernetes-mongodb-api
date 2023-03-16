# 8-mega-kubernetes-node.js-crud

The content given in this folder can be used to deploy a node.js application ([1k-crud](../code.dev)) on a kubernetes cluster.  A python based simple automation toolset is also provided. Directory structure is as below:

```
├── code.dev
│   ├── app.js
│   ├── Dockerfile
│   ├── modules
│   │   └── mongodb.util.js
│   └── package.json
├── k8s.resources
│   ├── python
│   │   ├── config
│   │   │   ├── config.json
│   │   ├── deploy.sh
│   │   ├── py
│   │   │   ├── configmap.py
│   │   │   ├── deployment.py
│   │   │   ├── get-version.py
│   │   │   ├── ingress.py
│   │   │   └── service.py
│   │   ├── template
│   │   │   ├── configmap.template.yaml
│   │   │   ├── deployment.template.yaml
│   │   │   ├── ingress.template.yaml
│   │   │   └── service.template.yaml
│   │   └── yaml
│   │       ├── configmap.yaml
│   │       ├── deployment.yaml
│   │       ├── ingress.yaml
│   │       └── service.yaml
│   └── README.md
├── README.md
└── todo.csv
```
## Installation Details

`config` folder contains  `.json` file which holds both packaging and mongdodb related settings.

```json
{
  "control": {
    "version": "1.0.6",
    "image-registry": "image-registry.1k.local",
    "resources": "configmap|deployment|ingress|service",
    "state": false
  },
  "mongodb-api": {
    "name": "mongodb-api",
    "namespace": "1k-hands",
    "labels": {
      "category": "microservice",
      "application": "mongodb-api",
      "resiliency": "single",
      "instance-id": "inst-0002"
    },
    "liveness-path": "healthy",
    "port": 22080
  },
  "configmap": {
    "data": {
      "DB_SERVER": "single-mongodb",
      "DB_PORT": "27017",
      "DB_NAME": "1k-sample",
      "APP_NAME": "1k-crud",
      "DB_REQUIRED": "name",
      "API_PORT": "22080"
    }
  },
  "ingress": {
    "host": "mongo.1k.local",
    "path": "/api",
    "pathType": "Exact"
  },
  "deployment": {
    "replicas": 3,
    "container-image": "image-registry.1k.local/microservice/1k-crud:1.0.6"
  },
  "service": {
    "type": "ClusterIP"
  }
}
```
- **control** section provides pacakage level settings
  - resources to be created
  - versioning and pipeline information
  - whether the database will be stateful or not
- ***mongodb-api** section includes common properties can will be used for multiple kubernetes resources
- There are specific sections for resource based properties.
---
`template` folder contains template kubernetes resource yamls. Each resource mention in `control.resources` attribute of `config.json` must have a corresponding template yaml in this folder.
Some of the fields in these templates will be filled by using the values from configuration file. Although it is not a parameter substition operation the fields to be filled are pre-filled with dummy values starting and ending with string `1k`.

---

`py` folder holds the python code files. Each resource mention in `control.resources` attribute of `config.json` must have a corresponding python code file in this folder. Functionality provided here is intentionally kept simple. Details of the python code will not be explained further. In case of questions please reach out to the author.

---

`yaml` folder holds the resulting kubernetes yaml files which are ready to be deployed. The folder being empty or not prior to deployment does not make any difference.

--- 

`deploy.sh` script performs the actions:
- build the docker image from `code.dev` directory and tag it and push to the image repository.
- read the list of resources to be created from `config.json`
- call python code from `py` folder to create the resource yaml under `yaml` folder
- call `kubectl apply -f ` with the resource yaml to create the resource at Kubernetes cluster.

Current state of `config.json` installs a stateless mongodb deployment and a kubernetes service under `1k-hands` namespace/

Kubernetes Resource List:

* ConfigMap 
* Deployment
* Ingress
* Service

Node.js ap[plication will be an api with `GET`, `POST`, `PUT`, and `DELETE` methods. Hostname of the application is provided under `ingress` section of the `config.json` file. The configmap provided holds an environment variable `APP_NAME` which is also the path used in ingress and also in Node.js code. There is an additional `/healthy` path which is utilized by the `liveness probe`.

## Configmap
A configmap will be defined and utilized in the applciation pod in form of environment variables. It will hold the following information:

| Variable| Description| Value|
|-|-|-|
|DB_SERVER|MongoDB Kuberneter Service Name|single-mongodb|
|DB_PORT|MongoDB Kuberneter Service Name|27017|
|DB_NAME|A custom name for the database|1k-sample|
|APP_NAME|A custom name for the applciation|1k-crud|
|DB_REQUIRED|Name of the `required` field for the database|name|
|API_PORT|TCP Port number listenned by Node.js|22080|
||||

## Deployment:
Node.js applciation will be deployed in `1k-hands` namespace with 3 replicas. Internal image registry will be used to pull the newly built container image from.

## Ingress:
An ingress with single rule (single hostname and path), pathType exact will be created. API is exposed as plain http.

## Service:
Service type will be `ClusterIP`. So it will be only accessible within k8s cluster

The outcome of running `deploy.sh` with the given `config.json` is as below:

```shell
$ kubectl -n 8-mega-hands-on get configmap mongodb-api         
NAME          DATA   AGE
mongodb-api   6      16s

$ kubectl -n 1k-hands get ingress mongodb-api  
NAME          CLASS    HOSTS                ADDRESS   PORTS   AGE
mongodb-api   <none>   mongo.8-mega.local             80      22s

$ kubectl -n 1k-hands get deployment mongodb-api
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
mongodb-api   3/3     3            3           31s

$ kubectl -n 1k-hands get pods | grep mongodb-api
mongodb-api-67c9548c8d-b2p85      1/1     Running   0          41s
mongodb-api-67c9548c8d-ftkgg      1/1     Running   0          41s
mongodb-api-67c9548c8d-wzxgg      1/1     Running   0          41s

$ kubectl -n 1k-hands get svc mongodb-api        
NAME          TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)     AGE
mongodb-api   ClusterIP   10.32.0.138   <none>        22080/TCP   49s

$ kubectl -n 1k-hands get ep | grep mongodb-api
mongodb-api      10.2.1.61:22080,10.2.3.73:22080,10.2.3.74:22080   58s
```