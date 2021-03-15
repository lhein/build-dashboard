import os
import json
import requests
import time

ENV_VAR_NAME = 'CIRCLECI_TOKEN'
ENV_VAR_UNDEFINED = 'UNDEFINED'

FUSE_QE_JENKINS = 'https://master-jenkins-csb-fusetools-qe.cloud.paas.psi.redhat.com'
DEVTOOLS_JENKINS = 'https://studio-jenkins-csb-codeready.cloud.paas.psi.redhat.com'
CIRCLECI_API_HOST = 'https://api.travis-ci.com'
CIRCLECI_HOST = 'https://travis-ci.com/'
CIRCLECI = 'Travis'
JENKINS = 'Jenkins'
JENKINS_FUSE_VSCODE_FOLDER = '/job/Fuse/job/VSCode/job/'

JOBS = [
	{ 'jobName': 'jbosstools-fuse_master', 						          'ci': DEVTOOLS_JENKINS,   					                'folder': '/job/Studio/job/Engineering/job/build_master/job/',   'type': JENKINS },
  { 'jobName': 'jbosstools-fuse-jdknext_master',              'ci': DEVTOOLS_JENKINS,   					                'folder': '/job/Studio/job/Engineering/job/build_jdkNext/job/',  'type': JENKINS },
	{ 'jobName': 'pullrequest-fuse', 	            			        'ci': DEVTOOLS_JENKINS,   					                'folder': '/job/Studio/job/Engineering/job/pr_checks/job/',      'type': JENKINS },
  { 'jobName': 'jbosstools-fuse-extras_master', 				      'ci': DEVTOOLS_JENKINS,			    		                'folder': '/job/Studio/job/Engineering/job/build_master/job/',   'type': JENKINS },
  { 'jobName': 'jbosstools-fuse-extras-jdknext_master',       'ci': DEVTOOLS_JENKINS,   					                'folder': '/job/Studio/job/Engineering/job/build_jdkNext/job/',  'type': JENKINS },
	{ 'jobName': 'pullrequest-fuse-extras',              		    'ci': DEVTOOLS_JENKINS,					                    'folder': '/job/Studio/job/Engineering/job/pr_checks/job/',      'type': JENKINS },
  { 'jobName': 'vscode-atlasmap-release', 					          'ci': DEVTOOLS_JENKINS, 							              'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
	{ 'jobName': 'vscode-camel-lsp-extension-pack-release', 	  'ci': DEVTOOLS_JENKINS, 							              'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
  { 'jobName': 'vscode-camel-lsp-release', 				            'ci': DEVTOOLS_JENKINS, 						    	          'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
  { 'jobName': 'vscode-camelk-release', 						          'ci': DEVTOOLS_JENKINS, 							              'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
  { 'jobName': 'vscode-didact-release', 					            'ci': DEVTOOLS_JENKINS, 							              'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
  { 'jobName': 'vscode-wsdl2rest-release', 					          'ci': DEVTOOLS_JENKINS, 							              'folder': JENKINS_FUSE_VSCODE_FOLDER,                            'type': JENKINS },
	{ 'jobName': 'camel-language-server', 						          'ci': 'camel-tooling/camel-language-server', 		    'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'camel-lsp-client-eclipse', 					          'ci': 'camel-tooling/camel-lsp-client-eclipse',     'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'camel-lsp-client-vscode', 					          'ci': 'camel-tooling/camel-lsp-client-vscode', 	    'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'camel-lsp-client-atom',						            'ci': 'camel-tooling/camel-lsp-client-atom',		    'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'vscode-wsdl2rest', 							              'ci': 'camel-tooling/vscode-wsdl2rest', 			      'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'vscode-atlasmap', 							              'ci': 'jboss-fuse/vscode-atlasmap', 				        'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'vscode-camelk', 								              'ci': 'camel-tooling/vscode-camelk', 				        'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'vscode-camel-extension-pack', 				        'ci': 'camel-tooling/vscode-camel-extension-pack', 	'folder': '/',                                                   'type': CIRCLECI },
	{ 'jobName': 'vscode-atlasmap-pipeline', 					          'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
	{ 'jobName': 'vscode-camelk-pipeline', 						          'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
	{ 'jobName': 'vscode-lsp-pipeline', 						            'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
	{ 'jobName': 'vscode-wsdl2rest-pipeline', 					        'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
	{ 'jobName': 'vscode-project-initializer-pipeline', 		    'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
	{ 'jobName': 'lsp-eclipse-client-nightly-matrix', 			    'ci': FUSE_QE_JENKINS, 								              'folder': '/job/vscode/job/',                                    'type': JENKINS },
  { 'jobName': 'fuse-smoke', 									                'ci': FUSE_QE_JENKINS, 							                'folder': '/job/',                                               'type': JENKINS }
]

def getCircleCIToken():
	return os.getenv(ENV_VAR_NAME, ENV_VAR_UNDEFINED)

def hasCircleCITokenDefined():
	return getCircleCIToken() != ENV_VAR_UNDEFINED

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

def fetchCircleCIStatus(url):
	token = getCircleCIToken()

	response = requests.get(url, headers={'User-Agent': 'CI-Dashboard', 'Travis-API-Version': '3' ,'Authorization': 'token ' + token}, verify=False, timeout=5)
	jobStatus = json.loads(response.text)

	return jobStatus

def fetchJenkinsStatus(url):
	response = requests.get(url, headers={'Accept': 'application/json'}, verify=False, timeout=5)
	jobStatus = json.loads(response.text)
	return jobStatus

def getJenkinsJobStatus(serverUrl, folderName, jobName):
	try:
		jobUrl = serverUrl + folderName + jobName
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

def getCircleCIJobStatus(repo, folderName, jobName):
	try:
		parts = repo.split('/')
		branch = fetchCircleCIStatus(CIRCLECI_API_HOST + '/repo/github/' + parts[0] + '%2F' + parts[1] + '/branch/master')
		lastBuild = branch['last_build']
		buildId = lastBuild['id']
		buildResult = mapToJenkinsStates(lastBuild['state'])
		last_build_number = lastBuild['number']

		jobUrl = CIRCLECI_HOST + 'github/' + repo + '/builds/'
		buildLink = jobUrl + str(buildId)

		return { 'name': jobName, 'buildNumber': str(last_build_number), 'buildStatus': buildResult, 'buildUrl': buildLink, 'jobUrl': jobUrl }
	except Exception as e:
		print(e)
		return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': CIRCLECI_HOST + repo + '/builds/' }

def getJobSkeleton(jobName):
	return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': '' }

def getAllJobNames():
	return list(map(lambda job: job['jobName'], JOBS))

def getJob(jobName):
	job = list(filter(lambda job: job['jobName'] == jobName, JOBS))[0]

	if job['type'] == JENKINS:
		jobStatus = getJenkinsJobStatus(job['ci'], job['folder'], jobName)
	elif job['type'] == CIRCLECI:
		jobStatus = getCircleCIJobStatus(job['ci'], job['folder'], jobName)
	else:
		jobStatus = None

	return jobStatus
