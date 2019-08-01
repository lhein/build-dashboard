import React, { useState, useEffect, useCallback } from 'react';
import { PageSection } from '@patternfly/react-core';
import { JobTable } from './JobTable';

function useApi(url, initialValue) {
  const [data, setData] = useState(initialValue);
  const readApi = useCallback(
    async function() {
      const result = await fetch(url, { mode: 'cors' });
      const resultObj = await result.json();
      setData(resultObj.jobs);
    },
    [url]
  );

  useEffect(() => {
    readApi();
    const runner = setInterval(readApi, 60000);
    return () => {
      clearInterval(runner);
    };
  }, [url, readApi]);
 
  return data;
}

const Dashboard: React.FunctionComponent = () => {
  let restAPIProvider = process.env.BACKEND;
  if (!restAPIProvider) {
    restAPIProvider = 'http://python-rest-api-fuse-dashboard.int.open.paas.redhat.com';
  }
  const JOBS_SERVICE_URL = restAPIProvider + '/ci-jobs/api/v1.0/jobs/';
  const jobs = useApi(JOBS_SERVICE_URL, []);
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
  }, [jobs, setFetchedJobs]);

  // patch jobs
  let patchedJobs = jobs.map( (currentValue, index, arr) => {
	  let idx = fetchedJobs.findIndex( (element) => {
		return element.name === currentValue.name;
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
