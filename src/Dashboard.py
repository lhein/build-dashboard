from flask import Flask, render_template, make_response, jsonify, abort
import CIUtils

def generateHTML(jobName, buildNumber, status, buildUrl, jobUrl):
	buildResult = str(status).upper()
	bgcolor = 'white'
	color = 'black'
	if (status == 'passed' or status == 'SUCCESS'):
		buildResult = 'OK'
		bgcolor = 'lightgreen'
	elif (status == 'failed' or status == 'FAILURE'):
		buildResult = "ERROR"
		bgcolor = 'red'
		color = 'white'
	elif (status == 'aborted' or status == 'ABORTED'):
		buildResult = "ABORTED"
		bgcolor = 'gray'
	return [ jobName, jobUrl, buildUrl, str("#" + buildNumber), buildResult, bgcolor, color ]

app = Flask(__name__, static_folder="../build/static", template_folder="../build")

@app.route("/")
def launch():
	return render_template('index.html')

@app.route("/static/js/<path:path>")
def templ(path):
	# mind the correct escaping of the json object. this is required by the double hop in javascript
	resp = make_response(render_template("./static/js/" + path))
	resp.headers['Content-type'] = 'text/javascript'
	return resp

@app.route('/ci-jobs/api/v1.0/jobs/', methods=['GET'])
def get_jobs():
	return jsonify({'jobs': CIUtils.getAllJobs()})

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
	app.debug=True
	app.run(host='0.0.0.0', use_reloader=True, port=50005, threaded=True)

