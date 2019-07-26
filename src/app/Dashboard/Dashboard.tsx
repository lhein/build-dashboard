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
  const JOBS_SERVICE_URL = 'http://0.0.0.0:50005/ci-jobs/api/v1.0/jobs/';
  const jobs = useApi(JOBS_SERVICE_URL, []);

  return (
    <PageSection>
      <JobTable data={jobs} />
    </PageSection>
  );
};

export { Dashboard };
