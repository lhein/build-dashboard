import json
import requests
from travispy import TravisPy
from flask import Flask, render_template, make_response

gitToken = '465c9b9acaeebb56b5b4eef445f6bcf1ddc27bfb'
fuseJenkins = 'https://fusesource-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
devToolsJenkins = 'https://dev-platform-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'

FUSE_JENKINS_JOBS = [
    'jbosstools-fuse_master',
    'jbosstools-fuse.sonar_master',
    'jbosstools-fuse_master-jdk11',
    'jbosstools-fuse_master-jdk12',
    'jbosstools-fuse_PullRequest',
    'jbosstools-fuse_PullRequest-OnlyTemplates',
    'fuse-components-camel-sap-7-4-x-checkin'
]

DEVTOOLS_JENKINS_JOBS = [
    'jbosstools-fuse-extras_master',
    'jbosstools-fuse-extras-Pull-Request',
    'vscode-apache-camel_release',
    'vscode-wsdl2rest-release',
    'vscode-atlasmap-release',
    'vscode-camelk-release',
    'vscode-apache-camel-extension-pack-release'
]

TRAVIS_JOBS = {
    'camel-language-server': 'camel-tooling/camel-language-server',
    'camel-tooling-common': 'camel-tooling/camel-tooling-common',
    'camel-lsp-client-eclipse': 'camel-tooling/camel-lsp-client-eclipse',
    'camel-lsp-client-vscode': 'camel-tooling/camel-lsp-client-vscode',
    'vscode-wsdl2rest': 'camel-tooling/vscode-wsdl2rest',
    'vscode-atlasmap': 'jboss-fuse/vscode-atlasmap',
    'vscode-camelk': 'camel-tooling/vscode-camelk',
    'vscode-camel-extension-pack': 'camel-tooling/vscode-camel-extension-pack'
}

def getJenkinsJobStatus(serverUrl, jobName):
	try:
		jobApiUrl = serverUrl + '/job/' + jobName + '/api/json'
		jobUrl = serverUrl + '/job/' + jobName
		response = requests.get(jobApiUrl, verify=False)
		jobStatus = json.loads(response.text)
		color = jobStatus['color']
		last_build_number = jobStatus['lastCompletedBuild']['number']
		buildLink = jobStatus['lastCompletedBuild']['url']
		buildResult = 'UNKNOWN'
		if (str(color).lower().startswith('blue')):
			buildResult = 'SUCCESS'
		elif (str(color).lower().startswith('red')):
			buildResult = 'FAILURE'
		elif (str(color).lower().startswith('aborted')):
			buildResult = 'ABORTED'
		return generateHTML(jobName, str(last_build_number), buildResult, buildLink, jobUrl)
	except Exception as e:
		return [ jobName, jobUrl, '', 'UNKNOWN', 'UNKNOWN', 'lightgray', 'black' ]

def getTravisJobStatus(repo, token, jobName):
	try:
		t = TravisPy.github_auth(token)
		r = t.repo(repo)
		build = t.build(r.last_build_id)
		return generateHTML(jobName, str(build['number']), build['state'], 'https://travis-ci.org/' + r['slug'] + '/builds/' + str(build['id']), 'https://travis-ci.org/' + r['slug'] + '/builds/')
	except Exception as e:
		return [ jobName, 'https://travis-ci.org/' + repo + '/builds/', '', 'UNKNOWN', 'UNKNOWN', 'lightgray', 'black' ]

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
	return render_template('index.html', MY_TOKEN=[ {'name': 'My Job', 'jobUrl': 'http://google.com', 'buildNumber': '#17', 'buildUrl': 'http://redhat.com', 'buildStatus': 'SUCCESS'}, ])

@app.route("/static/js/<path:path>")
def templ(path):
	# mind the correct escaping of the json object. this is required by the double hop in javascript
	resp = make_response(render_template("./static/js/" + path, MY_TOKEN='[ {\\"name\\": \\"My Job\\", \\"jobUrl\\": \\"http://google.com\\", \\"buildNumber\\": \\"#17\\", \\"buildUrl\\": \\"http://redhat.com\\", \\"buildStatus\\": \\"SUCCESS\\"} ]'))
	resp.headers['Content-type'] = 'text/javascript'
	return resp

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', use_reloader=True, port=50005, threaded=True)

def stale():
	job_list = []

	# get all the results from the Fuse Jenkins
	for job in FUSE_JENKINS_JOBS:
		job_list.append(getJenkinsJobStatus(fuseJenkins, job))

	# get all the results from the DevTools Jenkins
	for job in DEVTOOLS_JENKINS_JOBS:
		job_list.append(getJenkinsJobStatus(devToolsJenkins, job))

	# get all the results from Travis
	for job, repo in TRAVIS_JOBS.items():
		job_list.append(getTravisJobStatus(repo, gitToken, job))

	return render_template('index.html')
	
