import os
import json
import requests
import time

FUSE_JENKINS = 'https://fusesource-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
FUSE_QE_JENKINS = 'https://master-jenkins-csb-fusetools-qe.cloud.paas.psi.redhat.com'
DEVTOOLS_JENKINS = 'https://dev-platform-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
NEW_DEVTOOLS_JENKINS = 'https://studio-jenkins-csb-codeready.cloud.paas.psi.redhat.com'
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
	{ 'jobName': 'vscode-atlasmap-pipeline', 					          'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-camelk-pipeline', 						          'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-lsp-pipeline', 						            'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-wsdl2rest-pipeline', 					        'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'vscode-project-initializer-pipeline', 		    'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
	{ 'jobName': 'lsp-eclipse-client-nightly-matrix', 			    'ci': FUSE_QE_JENKINS, 								              'type': JENKINS },
  { 'jobName': 'fuse-smoke', 									                'ci': FUSE_QE_JENKINS, 							                'type': JENKINS }
]

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

def fetchJenkinsStatus(url):
	response = requests.get(url, headers={'Accept': 'application/json'}, verify=False, timeout=5)
	jobStatus = json.loads(response.text)
	return jobStatus

def getJenkinsJobStatus(serverUrl, jobName):
	try:
		jobUrl = serverUrl + '/job/Fuse/job/VSCode/job/' + jobName
		if (serverUrl != NEW_DEVTOOLS_JENKINS):
			jobUrl = serverUrl + '/job/' + jobName + '/api/json'
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

def getJobSkeleton(jobName):
	return { 'name': jobName, 'buildNumber': 'UNKNOWN', 'buildStatus': 'UNKNOWN', 'buildUrl': '', 'jobUrl': '' }

def getAllJobNames():
	return list(map(lambda job: job['jobName'], JOBS))

def getJob(jobName):
	job = list(filter(lambda job: job['jobName'] == jobName, JOBS))[0]

	if job['type'] == JENKINS:
		jobStatus = getJenkinsJobStatus(job['ci'], jobName)
	else:
		jobStatus = None

	return jobStatus
