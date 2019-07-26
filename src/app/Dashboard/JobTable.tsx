import React, { useState, useEffect, useCallback } from 'react';
import { Alert } from '@patternfly/react-core';
import { StyledText } from '@patternfly/react-styled-system';
import {
  Table,
  TableHeader,
  TableBody,
  sortable,
  SortByDirection,
  TableVariant,
  textCenter
} from '@patternfly/react-table';
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
    props: { className: 'pf-u-text-align-right' },
    transforms: [sortable, textCenter],
    cellTransforms: [textCenter]
  },
  {
    title: 'Build No.',
    transforms: [textCenter],
    cellTransforms: [textCenter]
  },
  {
    title: 'State'
  }
];

function toRow(job) {
  const jobName = job.name;
  const jobUrl = job.jobUrl;
  const buildNumber = job.buildNumber;
  const buildUrl = job.buildUrl;
  const buildStatus = job.buildStatus;

  const row = [];

  row.push({ title: <a href={jobUrl}>{jobName}</a> });
  row.push({ title: <a href={buildUrl}>{buildNumber}</a> });

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

  return row;
}

const JobTable: React.FunctionComponent = ({ data }) => {
  let rows = [];
  const [sortBy, setSortBy] = useState({});
  const [selectedRows, setSelectedRows] = useState([]);

  const onSelect = (event, isSelected, rowId, rowData, extraData) => {
    if (isSelected) {
      setSelectedRows(Array.from(new Set([...selectedRows, rowId])));
    } else {
      setSelectedRows(selectedRows.filter(id => id === rowId));
    }
  };

  const onSort = (_event, index, direction) => {
    setSortBy({
      index,
      direction
    });
  };

  const setIsSelected = row => {
    console.log(row);
    return {
      ...row,
      isSelected: selectedRows.find(row.id) ? true : false
    };
  };

  const sortRows = (a, b) => {
    // rows: direction === SortByDirection.asc ? sortedRows : sortedRows.reverse()
    a.name.localeCompare(b.name);
  };

  rows = data
    .map(toRow)
    .map(setIsSelected)
    .sort(sortRows);

  const jobsInTrouble = 0;

  return (
    <div>
      {jobsInTrouble > 0 && <Alert variant="warning" isInline={true} title="There are jobs in trouble!" />}
      <Table variant="compact" cells={columns} rows={rows} onSelect={onSelect} sortBy={sortBy} onSort={onSort}>
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
