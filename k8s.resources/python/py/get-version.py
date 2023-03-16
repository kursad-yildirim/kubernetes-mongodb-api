import json;
import sys;

# Read config json file
with open('./config/config.json', 'r') as configJsonFile:
        fullConfig = json.load(configJsonFile);
        configJsonFile.close();

currentVersion = json.dumps(fullConfig['control']['version']).strip('"').split('.');

if sys.argv[1] in 'major':
    currentVersion[0] = str(int(currentVersion[0]) + 1);
elif sys.argv[1] in 'minor':
    currentVersion[1] = str(int(currentVersion[1]) + 1);
else:
    currentVersion[2] = str(int(currentVersion[2]) + 1);
fullConfig['control']['version'] = currentVersion[0] + '.' + currentVersion[1] + '.' + currentVersion[2] ;
fullConfig['deployment']['container-image'] = json.dumps(fullConfig['control']['image-registry']).strip('"') + '/' + json.dumps(fullConfig['mongodb-api']['labels']['category']).strip('"') + '/' + json.dumps(fullConfig['configmap']['data']['APP_NAME']).strip('"') + ':' + json.dumps(fullConfig['control']['version']).strip('"');

with open('./config/config.json', 'w') as configJsonFile:
            json.dump(fullConfig,configJsonFile,indent=2);
            configJsonFile.close();
