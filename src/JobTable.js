import React from 'react';
import JobRow from "./JobRow";
import './JobTable.css';

class JobTable extends React.Component {
	render() {
		const rows = [];

		this.props.jobs.forEach((job) => {
			rows.push(
				<JobRow
					job={job}
					key={job.name} />
			);
		});

		return (
			<table>
				<thead>
					<tr>
						<th>Jobname</th>
						<th class="right-align-me">Build No.</th>
						<th class="center-me">Status</th>
					</tr>
				</thead>
				<tbody>{rows}</tbody>
			</table>
		);
	}
}

export default JobTable;