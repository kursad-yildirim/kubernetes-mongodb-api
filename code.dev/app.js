var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var router = express.Router();
const targetDB = require('./modules/mongodb.util');
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
targetDB.init();
var dbData = {};
const databaseName = process.env.DB_NAME;
const appName = process.env.APP_NAME;
const requiredFieldName = process.env.DB_REQUIRED;
const apiPort = process.env.API_PORT;

app.use('/', router);
//===== HEALTH =====//
router.route('/healthy').get(function(req, res, next){
        res.json([{operationName: 'healthy', operationStatus: 'OK'}]);
        });
//===== GET =====//
router.route('/' + appName).get(function(req, res, next){
	var queryString = {};
	var columnSelect = {_id: 0};
	if (req.query.hasOwnProperty(requiredFieldName)){
		if (req.query[requiredFieldName].length > 0){
			queryString = { [requiredFieldName]: req.query[requiredFieldName] }
			columnSelect = {_id: 0, __v: 0};
		}
	}
	targetDB[databaseName].find(queryString,columnSelect).then(success).catch(failure);
	function success(data){
                if (data.length == 0){
                        res.json([{name: 'No record found!'}]);
                        console.log('GET-Request: 0 Results');
                } else {
                        res.json(data);
                        console.log('GET-Request: ' + data.length + ' Results');
                }
	}
	function failure(error){
		res.json([{operationName: 'read', operationStatus: 'Error-101'}]);
	}
});

//===== POST =====//
router.route('/' + appName).post(function(req, res, next){
        targetDB[databaseName].create(req.body).then(success).catch(failure);
        function success(data){
                res.json({operationName: 'create', operationStatus: 'ok'});
        }
        function failure(error){
                res.json({operationName: 'create', operationStatus: 'Error-101'});
        }
});

//===== PUT =====//
router.route('/' + appName).put(function(req, res, next){
        targetDB[databaseName].findOneAndUpdate({[requiredFieldName]: req.body.name }, req.body,{new: true, upsert:true}).then(success).catch(failure);
        function success(data){
                        res.json({operationName: 'update', operationStatus: 'ok'});
        }
        function failure(error){
                        res.json({operationName: 'update', operationStatus: 'Error-101'});
        }
});

//===== DELETE =====//
router.route('/' + appName).delete(function(req, res, next){
        targetDB[databaseName].deleteMany(req.body).then(success).catch(failure);
        function success(data){
                res.json({operationName: 'delete', operationStatus: 'ok'});
        }
        function failure(error){
                res.json({operationName: 'delete', operationStatus: 'Error-101'});
        }
});

var server = app.listen(apiPort, function (){
	console.log('Server running at port:' + apiPort + '/');
});
