import React, { useState, useEffect, useCallback } from 'react';
import {
	Alert, 
	PageSection,
} from '@patternfly/react-core';
import { PatternFlyThemeProvider, StyledConstants, StyledBox, StyledText } from '@patternfly/react-styled-system';
import {
	Table,
	TableHeader,
	TableBody,
	sortable,
	SortByDirection,
	headerCol,
	TableVariant,
	expandable,
	cellWidth,
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


function useApi(url, initialValue) {
	const [data, setData] = useState(initialValue);
	const readApi = useCallback(
		async function () {
			const result = await fetch(url, { mode: 'cors' });
			const resultObj = await result.json();
			setData(resultObj.jobs);
		},
		[url]
	);

	useEffect(() => {
		setTimeout(readApi, 500);
	}, [url, readApi]);

	return data;
}

const Dashboard: React.FunctionComponent = () => {

	const JOBS_SERVICE_URL = 'http://0.0.0.0:50005/ci-jobs/api/v1.0/jobs/';
	const jobs = useApi(JOBS_SERVICE_URL, []);

	const columns = [
		{
			title: 'Jobname',
			transforms: [textCenter],
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
	const jobsInTrouble = 0;

	for (let job of jobs) {
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

		rows.push(row);
	}

	return (
		<PageSection>
			{jobsInTrouble > 0 && <Alert variant="warning" isInline title='There are jobs in trouble!' />}
			<Table variant="compact" cells={columns} rows={rows} >
				<TableHeader />
				<TableBody />
			</Table>
			{jobs.length === 0 && <div><br/><br/><center><SpinnerAltIcon key="icon" />&nbsp;Loading...</center></div>}
		</PageSection>
	);
}

export { Dashboard };
