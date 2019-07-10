import React from 'react';

class SearchBar extends React.Component {
	render() {
		return (
			<form>
				<input type="text" placeholder="Search..." />
			</form>
		);
	}
}

export default SearchBar;