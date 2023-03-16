import json;
import yaml;

# Read config json file
with open('./config/config.json', 'r') as mongoDbApiConfigJsonFile:
        mongoDbApiConfig = json.load(mongoDbApiConfigJsonFile);
mongoDbApiConfigJsonFile.close();
# Read configmap yaml template file
with open('./template/configmap.template.yaml', 'r') as mongoDbApiConfigmapTemplateFile:
        mongoDbApiConfigmapYaml = yaml.safe_load(mongoDbApiConfigmapTemplateFile);
mongoDbApiConfigmapTemplateFile.close();
# Construct configmap yaml
mongoDbApiConfigmapYaml['metadata']['name'] = mongoDbApiConfig['mongodb-api']['name'];
mongoDbApiConfigmapYaml['metadata']['namespace'] = mongoDbApiConfig['mongodb-api']['namespace'];
mongoDbApiConfigmapYaml['metadata']['labels'] = yaml.safe_load(json.dumps(mongoDbApiConfig['mongodb-api']['labels']));
mongoDbApiConfigmapYaml['data'] = yaml.safe_load(json.dumps(mongoDbApiConfig['configmap']['data']));
# Write configmap yaml file
with open('./yaml/configmap.yaml', 'w') as mongoDbApiConfigmapFile:
        result = yaml.dump(mongoDbApiConfigmapYaml, mongoDbApiConfigmapFile)
mongoDbApiConfigmapFile.close();

