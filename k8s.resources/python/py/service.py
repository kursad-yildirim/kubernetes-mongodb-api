import json;
import yaml;

# Read config json file
with open('./config/config.json', 'r') as mongoDbApiConfigJsonFile:
        mongoDbApiConfig = json.load(mongoDbApiConfigJsonFile);
mongoDbApiConfigJsonFile.close();
# Read service yaml template file
with open('./template/service.template.yaml', 'r') as mongoDbApiServiceTemplateFile:
        mongoDbApiServiceYaml = yaml.safe_load(mongoDbApiServiceTemplateFile);
mongoDbApiServiceTemplateFile.close();
# Construct service yaml
mongoDbApiServiceYaml['metadata']['name'] = mongoDbApiConfig['mongodb-api']['name'];
mongoDbApiServiceYaml['metadata']['namespace'] = mongoDbApiConfig['mongodb-api']['namespace'];
mongoDbApiServiceYaml['metadata']['labels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiServiceYaml['spec']['selector'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiServiceYaml['spec']['type'] = yaml.safe_load(json.dumps(mongoDbApiConfig['service']['type']));
mongoDbApiServiceYaml['spec']['ports'][0]['port'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['port']));
mongoDbApiServiceYaml['spec']['ports'][0]['targetPort'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['port']));
# Write service yaml file
with open('./yaml/service.yaml', 'w') as mongoDbApiServiceFile:
        result = yaml.dump(mongoDbApiServiceYaml, mongoDbApiServiceFile)
mongoDbApiServiceFile.close();

