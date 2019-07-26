import React, { useState } from 'react';
import { Alert } from '@patternfly/react-core';
import { StyledText } from '@patternfly/react-styled-system';
import { Table, TableHeader, TableBody, sortable } from '@patternfly/react-table';
import {
  OutlinedCheckCircleIcon,
  OutlinedQuestionCircleIcon,
  OutlinedTimesCircleIcon,
  OutlinedGrimaceIcon,
  OutlinedHandPaperIcon
} from '@patternfly/react-icons';
import loader from '@app/loader.gif';

const columns = [
  {
    title: 'Jobname',
    transforms: [sortable]
  },
  {
    title: 'Build No.'
  },
  {
    title: 'State'
  },
  {
    title: ''
  }
];

function toTableRow(job) {
  const jobName = job.name;
  const jobUrl = job.jobUrl;
  const buildNumber = job.buildNumber;
  const buildUrl = job.buildUrl;
  const buildStatus = job.buildStatus;

  const row = [];

  row.push({ title: <a href={jobUrl}>{jobName}</a> });
  row.push({ title: <a href={buildUrl}>{buildNumber}</a> });

  row.trouble = false;
  if (buildStatus === 'SUCCESS') {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#486b00">
            <OutlinedCheckCircleIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
  } else if (buildStatus === 'FAILURE') {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#c9190b">
            <OutlinedTimesCircleIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
    row.trouble = true;
  } else if (buildStatus === 'ABORTED') {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#004368">
            <OutlinedHandPaperIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
  } else if (buildStatus === 'UNSTABLE') {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#795600">
            <OutlinedGrimaceIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
    row.trouble = true;
  } else if (buildStatus === 'NOT_BUILT') {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#151515">
            <OutlinedQuestionCircleIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
  } else {
    row.push({
      title: (
        <React.Fragment>
          <StyledText fontWeight="bold" color="#151515">
            <OutlinedQuestionCircleIcon key="icon" />
            &nbsp;{buildStatus}
          </StyledText>
        </React.Fragment>
      )
    });
  }

  row.rowKey = jobName;
  row.selected = job.selected;

  return row;
}

async function queryJob(jobName) {
  const JOB_SERVICE_URL = 'http://0.0.0.0:50005/ci-jobs/api/v1.0/jobs/' + jobName;
  const result = await fetch(JOB_SERVICE_URL, { mode: 'cors' });
  const resultObj = await result.json();
  return resultObj.job;
}

const JobTable: React.FunctionComponent<{ data: any[] }> = ({ data }) => {
  const [sortBy, setSortBy] = useState<any>({});

  const onSort = (event, index, direction) => {
    setSortBy({
      index,
      direction
    });
  };

  const sortRows = (a, b) => {
    if (sortBy.direction === 'asc') {
      return a.name.localeCompare(b.name);
    } else if (sortBy.direction === 'desc') {
      return b.name.localeCompare(a.name);
    } else {
      return 0;
    }
  };

  const reloadJob = (event, rowId, rowData, extra) => {
    const jobName = rowData.rowKey;
    const freshJob = queryJob(jobName);
    const newRow = toTableRow(freshJob);
    rows.splice(rowId, 1, newRow);
  };

  const rows = data.sort(sortRows).map(toTableRow);

  const jobsInTrouble = rows.filter(row => {
    return row.trouble === true;
  }).length;

  const actions = [
    {
      title: 'Reload',
      onClick: reloadJob
    }
  ];

  return (
    <div>
      {jobsInTrouble > 0 && <Alert variant="warning" isInline={true} title={`${jobsInTrouble} job(s) in trouble!`} />}
      <Table variant="compact" cells={columns} rows={rows} actions={actions} sortBy={sortBy} onSort={onSort}>
        <TableHeader />
        <TableBody />
      </Table>
      {data.length === 0 && (
        <div>
          <br />
          <br />
          <center>
            <img src={loader} alt="Content loading " />
          </center>
        </div>
      )}
    </div>
  );
};

export { JobTable };
