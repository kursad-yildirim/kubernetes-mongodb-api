#!/bin/bash

python3 ./py/get-version.py fix
IMAGE_REGISTRY_PUSH="default-route-openshift-image-registry.apps.tuff.tripko.local"
IMAGE_REGISTRY_PULL="image-registry.openshift-image-registry.svc:5000"

CATEGORY=`cat config/config.json | grep category | awk -F "\"" '{print $4}'`
APP_NAME=`cat config/config.json | grep APP_NAME | awk -F "\"" '{print $4}'`
IMAGE_NAME_PUSH="$IMAGE_REGISTRY_PUSH/$CATEGORY/$APP_NAME"
IMAGE_NAME_PULL="$IMAGE_REGISTRY_PULL/$CATEGORY/$APP_NAME"
VERSION=`cat config/config.json | grep version | awk -F "\"" '{print $4}'`
IMAGE_TAG_PUSH="$IMAGE_NAME_PUSH:$VERSION"
IMAGE_TAG_PULL="$IMAGE_NAME_PULL:$VERSION"

sudo docker build -t $IMAGE_TAG_PUSH ../../code.dev/ > /dev/null 2>&1
sudo docker push $IMAGE_TAG_PUSH > /dev/null 2>&1

RESOURCE_LIST=`cat config/config.json | grep resources | awk -F "\"" '{print $4}'`

IFS='|' read -r -a RESOURCE_LIST_ARRAY <<< "$RESOURCE_LIST"

for RESOURCE in "${RESOURCE_LIST_ARRAY[@]}"
do
	python3 ./py/$RESOURCE.py
	kubectl apply -f ./yaml/$RESOURCE.yaml
done

