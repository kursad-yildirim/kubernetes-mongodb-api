import json;
import yaml;

# Read config json file
with open('./config/config.json', 'r') as mongoDbApiConfigJsonFile:
        mongoDbApiConfig = json.load(mongoDbApiConfigJsonFile);
mongoDbApiConfigJsonFile.close();
# Read deployment yaml template file
with open('./template/deployment.template.yaml', 'r') as mongoDbApiDeployTemplateFile:
        mongoDbApiDeployYaml = yaml.safe_load(mongoDbApiDeployTemplateFile);
mongoDbApiDeployTemplateFile.close();
# Construct deployment yaml
mongoDbApiDeployYaml['metadata']['name'] = mongoDbApiConfig['mongodb-api']['name'];
mongoDbApiDeployYaml['metadata']['namespace'] = mongoDbApiConfig['mongodb-api']['namespace'];
mongoDbApiDeployYaml['metadata']['labels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiDeployYaml['spec']['replicas'] = yaml.safe_load(json.dumps(mongoDbApiConfig['deployment']['replicas']));
mongoDbApiDeployYaml['spec']['selector']['matchLabels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiDeployYaml['spec']['template']['metadata']['labels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiDeployYaml['spec']['template']['spec']['containers'][0]['image'] = yaml.safe_load(json.dumps(mongoDbApiConfig['deployment']['container-image']));
mongoDbApiDeployYaml['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['port']));
mongoDbApiDeployYaml['spec']['template']['spec']['containers'][0]['envFrom'][0]['configMapRef']['name'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['name']));
mongoDbApiDeployYaml['spec']['template']['spec']['containers'][0]['livenessProbe']['httpGet']['path'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['liveness-path']));
mongoDbApiDeployYaml['spec']['template']['spec']['containers'][0]['livenessProbe']['httpGet']['port'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['port']));
# Write deployment yaml file
with open('./yaml/deployment.yaml', 'w') as mongoDbApiDeployFile:
        result = yaml.dump(mongoDbApiDeployYaml, mongoDbApiDeployFile)
mongoDbApiDeployFile.close();
