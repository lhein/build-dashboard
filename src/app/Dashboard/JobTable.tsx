import React, { useState, useEffect, useCallback } from 'react';
import { Alert } from '@patternfly/react-core';
import { PatternFlyThemeProvider, StyledConstants, StyledBox, StyledText } from '@patternfly/react-styled-system';
import {
  Table,
  TableHeader,
  TableBody,
  sortable,
  SortByDirection,
  TableVariant,
  textCenter,
} from '@patternfly/react-table';
import {
  OutlinedCheckCircleIcon,
  OutlinedQuestionCircleIcon,
  OutlinedTimesCircleIcon,
  OutlinedGrimaceIcon,
  OutlinedHandPaperIcon,
  SpinnerAltIcon,
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

function toTableRow(job) {
  let jobName = job.name;
  let jobUrl = job.jobUrl;
  let buildNumber = job.buildNumber;
  let buildUrl = job.buildUrl;
  let buildStatus = job.buildStatus;

  let row = [];

  row.push({ title: <a href={jobUrl}>{jobName}</a> })
  row.push({ title: <a href={buildUrl}>{buildNumber}</a> });

  if (buildStatus === 'SUCCESS') {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#486b00"><OutlinedCheckCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  } else if (buildStatus === 'FAILURE') {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#c9190b"><OutlinedTimesCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  } else if (buildStatus === 'ABORTED') {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#004368"><OutlinedHandPaperIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  } else if (buildStatus === 'UNSTABLE') {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#795600"><OutlinedGrimaceIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  } else if (buildStatus === 'NOT_BUILT') {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#151515"><OutlinedQuestionCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  } else {
    row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#151515"><OutlinedQuestionCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
  }

  row.rowKey = jobName;
  row.selected = job.selected;

  return row;
}

const JobTable: React.FunctionComponent<{ data: any[] }> = ({ data }) => {
  const [sortBy, setSortBy] = useState<any>({});
  const [selectedRows, setSelectedRows] = useState<string[]>([]);

  const onSelect = (event, isSelected, rowIdx, rowData) => {
    if (isSelected) {
      setSelectedRows(
        Array.from(new Set([...selectedRows, rowData.rowKey]))
      );
    } else {
      setSelectedRows(
        selectedRows.filter(name => name !== rowData.rowKey)
      )
    }
  }

  const onSort = (_event, index, direction) => {
    setSortBy({
      index,
      direction
    });
  };

  const setIsSelected = (row) => {
    return {
      ...row,
      selected: !!selectedRows.find(name => name === row.name)
    }
  };

  const sortRows = (a, b) => {
    if (sortBy.direction === 'asc') {
      return a.name.localeCompare(b.name)
    } else if (sortBy.direction === 'desc') {
      return b.name.localeCompare(a.name)
    } else {
      return 0;
    }
  };

  const rows = data
    .map(setIsSelected)
    .sort(sortRows)
    .map(toTableRow);

  const jobsInTrouble = 0;

  return (
    <div>
      { jobsInTrouble > 0 && <Alert variant="warning" isInline title='There are jobs in trouble!' /> }
      <Table variant="compact" cells={columns} rows={rows} onSelect={onSelect} sortBy={sortBy} onSort={onSort} >
        <TableHeader />
        <TableBody />
      </Table>
      {data.length === 0 && <div><br/><br/><center><img src={loader} alt="Content loading "/></center></div>}
    </div>
  );
}

export { JobTable };
