import React, { useState, useEffect, useCallback } from 'react';
import { PageSection } from '@patternfly/react-core';
import { JobTable } from './JobTable';

async function callApi(url) {
  const response = await fetch(url, { mode: 'cors' });
  return await response.json();
}

function useJobs(baseUrl: string): [any[], (jobName: string) => Promise<void>] {
  const JOBS_SERVICE_URL = baseUrl + '/ci-jobs/api/v1.0/jobs/';
  const [allJobs, setAllJobs] = useState<string[]>([]);
  const [fetchedJobs, setFetchedJobs] = useState<{ [key: string]: any }>({});

  const fetchAllJobs = useCallback(
    async function() {
      const { jobs } = await callApi(JOBS_SERVICE_URL);
      setAllJobs(jobs);      
    },
    [JOBS_SERVICE_URL, setAllJobs]
  );

  const handleJobReload = useCallback(
    async function (jobName) {
      const { job } = await callApi(JOBS_SERVICE_URL + jobName);
      setFetchedJobs(previousFetchedJobs => ({
        ...previousFetchedJobs,
        [job.name]: job
      }));
    },
    [fetchedJobs, setFetchedJobs]
  );
  
  useEffect(() => {
    fetchAllJobs();
    // set a 5 minute timer for refresh
    const runner = setInterval(fetchAllJobs, 300000);
    return () => {
      clearInterval(runner);
    };
  }, [fetchAllJobs]);

  useEffect(() => {
      allJobs.map(job => handleJobReload(job));
    },
    [allJobs]
  );
  
  // patch jobs
  const patchedJobs = allJobs.map((job, index, arr) => 
    fetchedJobs[job] ? fetchedJobs[job] : { name: job }
  );

  return [patchedJobs, handleJobReload];
}

const Dashboard: React.FunctionComponent = () => {
  const baseUrl = !process.env.BACKEND ? 'http://0.0.0.0:50005' : 'http://python-rest-api-fuse-dashboard.int.open.paas.redhat.com';
  const [jobs, reloadJob] = useJobs(baseUrl);
  return (
    <PageSection>
      <JobTable data={jobs} onJobReload={reloadJob} />
    </PageSection>
  );
};

export { Dashboard };