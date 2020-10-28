import os
import json
import requests
import time

ENV_VAR_NAME = 'TRAVIS_TOKEN'
ENV_VAR_UNDEFINED = 'UNDEFINED'

FUSE_JENKINS = 'https://fusesource-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
FUSE_QE_JENKINS = 'https://master-jenkins-csb-fusetools-qe.cloud.paas.psi.redhat.com'
DEVTOOLS_JENKINS = 'https://dev-platform-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
NEW_DEVTOOLS_JENKINS = 'https://studio-jenkins-csb-codeready.cloud.paas.psi.redhat.com'
TRAVIS_API_HOST = 'https://api.travis-ci.com'
TRAVIS_HOST = 'https://travis-ci.com/'
TRAVIS = 'Travis'
JENKINS = 'Jenkins'

JOBS = [
	{ 'jobName': 'jbosstools-fuse_master', 						          'ci': FUSE_JENKINS, 								                'type': JENKINS },
	{ 'jobName': 'jbosstools-fuse.sonar_master', 				        'ci': FUSE_JENKINS, 								                'type': JENKINS },
	{ 'jobName': 'jbosstools-fuse_PullRequest', 				        'ci': FUSE_JENKINS, 								                'type': JENKINS },
	{ 'jobName': 'jbosstools-fuse_PullRequest-OnlyTemplates',   'ci': FUSE_JENKINS, 								                'type': JENKINS },
	{ 'jobName': 'jbosstools-fuse-extras_master', 				      'ci': DEVTOOLS_JENKINS, 						                'type': JENKINS },
	{ 'jobName': 'jbosstools-fuse-extras-Pull-Request', 		    'ci': DEVTOOLS_JENKINS, 						                'type': JENKINS },
	{ 'jobName': 'vscode-camel-lsp-release', 				            'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
	{ 'jobName': 'vscode-camel-lsp-extension-pack-release', 	  'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
  { 'jobName': 'vscode-atlasmap-release', 					          'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
  { 'jobName': 'vscode-camelk-release', 						          'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
  { 'jobName': 'vscode-didact-release', 					            'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
  { 'jobName': 'vscode-wsdl2rest-release', 					          'ci': NEW_DEVTOOLS_JENKINS, 							          'type': JENKINS },
	{ 'jobName': 'camel-language-server', 						          'ci': 'camel-tooling/camel-language-server', 		    'type': TRAVIS },
	{ 'jobName': 'camel-lsp-client-eclipse', 					          'ci': 'camel-tooling/camel-lsp-client-eclipse',     'type': TRAVIS },
	{ 'jobName': 'camel-lsp-client-vscode', 					          'ci': 'camel-tooling/camel-lsp-client-vscode', 	    'type': TRAVIS },
	{ 'jobName': 'camel-lsp-client-atom',						            'ci': 'camel-tooling/camel-lsp-client-atom',		    'type': TRAVIS },
	{ 'jobName': 'vscode-wsdl2rest', 							              'ci': 'camel-tooling/vscode-wsdl2rest', 			      'type': TRAVIS },
	{ 'jobName': 'vscode-atlasmap', 							              'ci': 'jboss-fuse/vscode-atlasmap', 				        'type': TRAVIS },
	{ 'jobName': 'vscode-camelk', 								              'ci': 'camel-tooling/vscode-camelk', 				        'type': TRAVIS },
	{ 'jobName': 'vscode-camel-extension-pack', 				        'ci': 'camel-tooling/vscode-camel-extension-pack', 	'type': TRAVIS },
	{ 'jobName': 'vscode-atlasmap-pipeline', 					          'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-camelk-pipeline', 						          'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-lsp-pipeline', 						            'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-wsdl2rest-pipeline', 					        'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-project-initializer-pipeline', 		    'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'lsp-eclipse-client-nightly-matrix', 			    'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
  { 'jobName': 'fuse-smoke', 									                'ci': FUSE_QE_JENKINS, 							                'type': JENKINS }
]

def getTravisToken():
	return os.getenv(ENV_VAR_NAME, ENV_VAR_UNDEFINED)

def hasTravisTokenDefined():
	return getTravisToken() != ENV_VAR_UNDEFINED

def mapToJenkinsStates(buildResult):
	mappedState = ''

	if (buildResult == 'passed'):
		mappedState = 'SUCCESS'
	elif (buildResult == 'canceled'):
		mappedState = 'ABORTED'
	elif (buildResult == 'failed'):
		mappedState = 'FAILURE'
	elif (buildResult == 'errored'):
		mappedState = 'FAILURE'
	else:
		mappedState = 'UNKNOWN'

	return mappedState

def fetchTravisStatus(url):
	token = getTravisToken()

	response = requests.get(url, headers={'User-Agent': 'CI-Dashboard', 'Travis-API-Version': '3' ,'Authorization': 'token ' + token}, verify=False, timeout=5)
	jobStatus = json.loads(response.text)

	return jobStatus

def fetchJenkinsStatus(url):
	response = requests.get(url, headers={'Accept': 'application/json'}, verify=False, timeout=5)
	jobStatus = json.loads(response.text)
	return jobStatus

def getJenkinsJobStatus(serverUrl, jobName):
	try:
		jobUrl = serverUrl + '/job/Fuse/job/VSCode/job/' + jobName
		jobApiUrl = jobUrl + '/api/json'
		jobStatus = fetchJenkinsStatus(jobApiUrl)
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

def getTravisJobStatus(repo, jobName):
	try:
		parts = repo.split('/')
		branch = fetchTravisStatus(TRAVIS_API_HOST + '/repo/' + parts[0] + '%2F' + parts[1] + '/branch/master')
		lastBuild = branch['last_build']
		buildId = lastBuild['id']
		buildResult = mapToJenkinsStates(lastBuild['state'])
		last_build_number = lastBuild['number']

		jobUrl = TRAVIS_HOST + repo + '/builds/'
		buildLink = jobUrl + str(buildId)


		return { 'name': jobName, 'buildNumber': str(last_build_number), 'buildStatus': buildResult, 'buildUrl': buildLink, 'jobUrl': jobUrl }
	except Exception as e:
		print(e)
		return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': TRAVIS_HOST + repo + '/builds/' }

def getJobSkeleton(jobName):
	return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': '' }

def getAllJobNames():
	return list(map(lambda job: job['jobName'], JOBS))

def getJob(jobName):
	job = list(filter(lambda job: job['jobName'] == jobName, JOBS))[0]

	if job['type'] == JENKINS:
		jobStatus = getJenkinsJobStatus(job['ci'], jobName)
	elif job['type'] == TRAVIS:
		jobStatus = getTravisJobStatus(job['ci'], jobName)
	else:
		jobStatus = None

	return jobStatus
