<h1> 8-mega-kubernetes-node.js-crud </h1>

This repo includes a simple node.js application that can be positioned in front of a MongoDB database to perform **C**reate-**R**eplace-**U**pdate-**D**elete operations. All operations will be performed in `1k-hands` namespace which has already been created.

The folder named as [code.dev](code.dev) includes source code and Dockerfile, while the folder named as [k8s.resources](k8s.resources) includes the content required to deploy the application to a kubernetes cluster. A simple python based automation tooling is also provided.

One of my repositories ([1K-mongodb](https://link)) can be used to deploy a single instance MongoDB database to a kubernetes cluster.