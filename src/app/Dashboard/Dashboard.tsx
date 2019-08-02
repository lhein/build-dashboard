import React, { useState, useEffect, useCallback } from 'react';
import { PageSection } from '@patternfly/react-core';
import { JobTable } from './JobTable';

const Dashboard: React.FunctionComponent = () => {
  let restAPIProvider = process.env.BACKEND;
  restAPIProvider = 'http://0.0.0.0:50005';
  if (!restAPIProvider) {
    restAPIProvider = 'http://python-rest-api-fuse-dashboard.int.open.paas.redhat.com';
  }

  const JOBS_SERVICE_URL = restAPIProvider + '/ci-jobs/api/v1.0/jobs/';
  const [jobNames, setJobNames] = useState( [] );
  const readApi = useCallback(
    async function() {
      const result = await fetch(JOBS_SERVICE_URL, { mode: 'cors' });
      const resultObj = await result.json();
      setJobNames(resultObj.jobs);
    }
  );
  
  useEffect(() => {
	readApi();

	// set a 5 minute timer for refresh
    const runner = setInterval(readApi, 300000); 
	
	return () => {
      clearInterval(runner);
    };
  }, [JOBS_SERVICE_URL, readApi]);

  const [fetchedJobs, setFetchedJobs] = useState([]);
  const handleJobReload = useCallback(
	async function(jobName) {
  	  let fj = [...fetchedJobs];
      const JOB_SERVICE_URL = JOBS_SERVICE_URL + jobName;
	  const result = await fetch(JOB_SERVICE_URL, { mode: 'cors' });
	  const resultObj = await result.json();
	  let job = resultObj.job;
	
	  let idx = fetchedJobs.findIndex( (element) => {
		return element.name === job.name;
	  });
	  if (idx!==-1) {
		fj.splice(idx, 1, job);
	  } else {
		fj.push(job);
	  }  
	  setFetchedJobs(fj);
	}
  );
  // drop patches when the all jobs data changes, which means that the interval triggered
  useEffect( () => {
   setFetchedJobs( [] );
  }, [jobNames, setFetchedJobs]);

  const fetchJobData = useCallback(
	async function() {
	  for (let jobName of jobNames) {
		  handleJobReload(jobName);
	  }
	},
	[jobNames]
  );

  useEffect(() => {
    fetchJobData();
  }, [jobNames, fetchJobData]);

  // patch jobs
  let patchedJobs = jobNames.map( (currentValue, index, arr) => {
	  let idx = fetchedJobs.findIndex( (element) => {
		return element.name === currentValue;
	  });
	  if (idx !== -1) {
		  return fetchedJobs[idx];
	  }
	  return currentValue;
  });

  return (
    <PageSection>
      <JobTable data={patchedJobs} onJobReload={handleJobReload} />
    </PageSection>
  );
};

export { Dashboard };
