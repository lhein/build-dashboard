from flask import Flask, render_template, make_response, jsonify, abort
from flask_cors import CORS
import CIUtils

app = Flask(__name__)
CORS(app)

@app.route('/ci-jobs/api/v1.0/jobs/', methods=['GET'])
def get_job_names():
	return jsonify({'jobs': CIUtils.getAllJobNames()})

#@app.route('/ci-jobs/api/v1.0/jobs/', methods=['GET'])
#def get_jobs():
#	return jsonify({'jobs': CIUtils.getAllJobs()})

@app.route('/ci-jobs/api/v1.0/jobs/<string:jobName>', methods=['GET'])
def get_job(jobName):
	job = CIUtils.getJob(jobName)
	if(job == None):
		abort(404)
	return jsonify({'job': job})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	if (CIUtils.hasGithubTokenDefined() == False):
		print('The environment variable ' + CIUtils.ENV_VAR_NAME + ' doesn\'t contain a valid GitHub OAuth Token! Exiting...')
		exit()

	app.debug=True
	app.run(host='0.0.0.0', use_reloader=True, port=50005, threaded=True)
