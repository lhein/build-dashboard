import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Dashboard from './Dashboard';
import * as serviceWorker from './serviceWorker';

let response = fetch('http://0.0.0.0:50005/ci-jobs/api/v1.0/jobs/');
let myJson = response.json(); //extract JSON from the http response
let jobs=JSON.parse(myJson);

//{% raw %}
ReactDOM.render(<Dashboard jobs={ jobs } />, document.getElementById('root'));
//{% endraw %}
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
