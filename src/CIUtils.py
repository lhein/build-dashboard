import os
import json
import requests
from travispy import TravisPy

gitToken = os.environ['GITHUB_TRAVIS_TOKEN']
fuseJenkins = 'https://fusesource-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
devToolsJenkins = 'https://dev-platform-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'

FUSE_JENKINS_JOBS = [
    'jbosstools-fuse_master',
    'jbosstools-fuse.sonar_master',
    'jbosstools-fuse_master-jdk11',
    'jbosstools-fuse_master-jdk12',
    'jbosstools-fuse_PullRequest',
    'jbosstools-fuse_PullRequest-OnlyTemplates',
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

def isFuseJenkinsJob(jobName):
	job = [job for job in FUSE_JENKINS_JOBS if job == jobName]
	return len(job) == 1

def isDevToolsJenkinsJob(jobName):
	job = [job for job in DEVTOOLS_JENKINS_JOBS if job == jobName]
	return len(job) == 1

def isTravisJob(jobName):
	for job, repo in TRAVIS_JOBS.items():
		if job == jobName:
			return True
	return False

def mapToJenkinsStates(buildResult):
	mappedState = ""
	if (buildResult == 'passed'):
		mappedState = "SUCCESS"
	elif (buildResult == 'canceled'):
		mappedState = "ABORTED"
	elif (buildResult == 'failed'):
		mappedState = "FAILURE"
	elif (buildResult == 'errored'):
		mappedState = "FAILURE"
	else:
		mappedState = "UNKNOWN"
	return mappedState

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
		return { 'name': jobName, 'buildNumber': str(last_build_number), 'buildStatus': buildResult, 'buildUrl': buildLink, 'jobUrl': jobUrl}
	except Exception as e:
		return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': jobUrl}

def getTravisJobStatus(repo, token, jobName):
	try:
		t = TravisPy.github_auth(token)
		r = t.repo(repo)
		build = t.build(r.last_build_id)
		last_build_number = str(build['number'])
		buildResult = mapToJenkinsStates(build['state'])
		buildLink = 'https://travis-ci.org/' + r['slug'] + '/builds/' + str(build['id'])
		jobUrl = 'https://travis-ci.org/' + r['slug'] + '/builds/'
		return { 'name': jobName, 'buildNumber': str(last_build_number), 'buildStatus': buildResult, 'buildUrl': buildLink, 'jobUrl': jobUrl}
	except Exception as e:
		return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': 'https://travis-ci.org/' + repo + '/builds/'}

def getAllJobs():
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
	
	return job_list

def getJob(jobName):
	job = {}
	if(isFuseJenkinsJob(jobName)):
		job = getJenkinsJobStatus(fuseJenkins, jobName)
	elif(isDevToolsJenkinsJob(jobName)):
		job = getJenkinsJobStatus(devToolsJenkins, jobName)
	elif(isTravisJob(jobName)):
		job = getTravisJobStatus(TRAVIS_JOBS[jobName], gitToken, jobName)
	else:
		job = None
	return job
