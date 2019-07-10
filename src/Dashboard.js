import React from 'react';
import './Dashboard.css';
import SearchBar from "./SearchBar";
import JobTable from "./JobTable";

class Dashboard extends React.Component {
	render() {
		return (
			<div className="Dashboard">
				<SearchBar />
				<JobTable jobs={this.props.jobs} />
			</div>
		);
	}
}

export default Dashboard;
