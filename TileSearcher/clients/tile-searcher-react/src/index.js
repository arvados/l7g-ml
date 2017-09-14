import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

document.body.style.backgroundColor = "#fafafa"
ReactDOM.render(
	<App />, 
	document.getElementById('root'));
registerServiceWorker();
