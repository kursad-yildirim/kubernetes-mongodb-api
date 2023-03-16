import json;
import yaml;

# Read config json file
with open('./config/config.json', 'r') as mongoDbApiConfigJsonFile:
        mongoDbApiConfig = json.load(mongoDbApiConfigJsonFile);
mongoDbApiConfigJsonFile.close();
# Read ingress yaml template file
with open('./template/ingress.template.yaml', 'r') as mongoDbApiIngressTemplateFile:
        mongoDbApiIngressYaml = yaml.safe_load(mongoDbApiIngressTemplateFile);
mongoDbApiIngressTemplateFile.close();
# Construct ingress yaml
mongoDbApiIngressYaml['metadata']['name'] = mongoDbApiConfig['mongodb-api']['name'];
mongoDbApiIngressYaml['metadata']['namespace'] = mongoDbApiConfig['mongodb-api']['namespace'];
mongoDbApiIngressYaml['metadata']['labels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiIngressYaml['spec']['rules'][0]['host'] = yaml.safe_load(json.dumps(mongoDbApiConfig['ingress']['host']));
mongoDbApiIngressYaml['spec']['rules'][0]['http']['paths'][0]['path'] = yaml.safe_load(json.dumps(mongoDbApiConfig['ingress']['path']));
mongoDbApiIngressYaml['spec']['rules'][0]['http']['paths'][0]['pathType'] = yaml.safe_load(json.dumps(mongoDbApiConfig['ingress']['pathType']));
mongoDbApiIngressYaml['spec']['rules'][0]['http']['paths'][0]['backend']['service']['name'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['name']));
mongoDbApiIngressYaml['spec']['rules'][0]['http']['paths'][0]['backend']['service']['port']['number'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['port']));

# Write ingress yaml file
with open('./yaml/ingress.yaml', 'w') as mongoDbApiIngressFile:
        result = yaml.dump(mongoDbApiIngressYaml, mongoDbApiIngressFile)
mongoDbApiIngressFile.close();