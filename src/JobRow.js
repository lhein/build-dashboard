import React from 'react';
import './JobTable.css';

class JobRow extends React.Component {
	render() {
		const job = this.props.job;
		const jobName = job.name;
		const jobUrl = job.jobUrl;
		const buildNumber = job.buildNumber;
		const buildUrl = job.buildUrl;
		const buildStatus = job.buildStatus;

		return (
			<tr>
				<td><a href="{jobUrl}">{jobName}</a></td>
				<td class="right-align-me"><a href="{buildUrl}">{buildNumber}</a></td>
				<td class="center-me" style="font-weight:bold">{buildStatus}</td>
			</tr>
		);
	}
}

export default JobRow;
