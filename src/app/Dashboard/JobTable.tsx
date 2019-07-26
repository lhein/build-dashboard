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

const jobsInTrouble = 0;
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
const rows = [];

function createJobEntry(job) {
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
		jobsInTrouble++;
		row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#c9190b"><OutlinedTimesCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
	} else if (buildStatus === 'ABORTED') {
		row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#004368"><OutlinedHandPaperIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
	} else if (buildStatus === 'UNSTABLE') {
		jobsInTrouble++;
		row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#795600"><OutlinedGrimaceIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
	} else if (buildStatus === 'NOT_BUILT') {
		row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#151515"><OutlinedQuestionCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
	} else {
		row.push({ title: (<React.Fragment><StyledText fontWeight="bold" color="#151515"><OutlinedQuestionCircleIcon key="icon" />&nbsp;{buildStatus}</StyledText></React.Fragment>) });
	}

	return row;
}

function onSelect(event, isSelected, rowId) {
	let rs;
    if (rowId === -1) {
      rs = rows.map(oneRow => {
        oneRow.selected = isSelected;
        return oneRow;
      });
    } else {
      rs = [...rows];
      rs[rowId].selected = isSelected;
    }
    setRows(rs);
}

const JobTable: React.FunctionComponent = ({data}) => {
	const [rows, setRows] = useState([rows]);
	const jobs = data;
	jobsInTrouble = 0;

	rows = jobs.map(createJobEntry);

	return (
		<div>
			{ jobsInTrouble > 0 && <Alert variant="warning" isInline title='There are jobs in trouble!' /> }
			<Table variant="compact" cells={columns} rows={rows} onSelect={onSelect} >
				<TableHeader />
				<TableBody />
			</Table>
			{jobs.length === 0 && <div><br/><br/><center><img src={loader} alt="Content loading "/></center></div>}
		</div>
	);
}

export { JobTable };
