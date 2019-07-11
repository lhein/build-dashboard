import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Dashboard from './Dashboard';
import * as serviceWorker from './serviceWorker';

let token=`{{ MY_TOKEN }}`;
// parse here is required because it's the only way to have webpack to accept the token we use above. it handles it as string and allows us to have anything in it, even the token.
let jobs=JSON.parse(token);

//{% raw %}
ReactDOM.render(<Dashboard jobs={ jobs } />, document.getElementById('root'));
//{% endraw %}
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
