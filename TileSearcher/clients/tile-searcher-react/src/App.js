import React, { Component } from 'react'
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import { FormComponent } from './FormComponent'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import AppBar from 'material-ui/AppBar';
import { ReferenceComponent } from './ReferenceComponent'
import { ResultsComponent } from './ResultsComponent'
import './App.css'
import { callApi } from "./Api"
import Paper from 'material-ui/Paper'
import CircularProgress from 'material-ui/CircularProgress'

injectTapEventPlugin()

const muiTheme = getMuiTheme({
	margin: 0,
	appBar: {
		height: 70
	},
});

class App extends Component {

	constructor(props) {
		super(props)
		this.handleSubmit = this.handleSubmit.bind(this)
		this.state = {
			resultsLoaded: false,
			responseJson: "",
			index: -1,
			loading: false
		}
		this.setLoading = this.setLoading.bind(this)
	}

	setLoading(state) {
		this.setState({
			loading: state
		})
	}

	handleSubmit(searchObject, callback) {
		this.setState({resultsLoaded: false})
		callApi(searchObject, (responseJson, err) => {
			if (err == null) {
				this.setState({
						responseLoaded: true,
						index: searchObject.index,
						responseJson: responseJson
					})
				callback(null)
			} else {
				this.setState({
					responseLoaded: true
				})
				callback(err)
			}
		})

	}

  	render() {
  		const responseLoader = <CircularProgress style={{margin: 8}} color="#fafafa"/>
    	return (
			<MuiThemeProvider muiTheme={muiTheme}>
		        <div>
		        	<AppBar
		        		title="Tile Searcher"
						style={{ margin: 0 }}
		        		showMenuIconButton={false}
		        		iconElementRight={this.state.loading ? responseLoader : null}/>
		        	<div style={{display: 'flex', flexDirection: 'row', flexWrap: 'wrap'}}>
					<Paper style={{margin: 16, height: 270}}>
						<FormComponent onSubmit={this.handleSubmit} 
							setLoading={this.setLoading}/>
					</Paper>
					<div>
						{this.state.responseLoaded ? <ResultsComponent json={this.state.responseJson} index={this.state.index}/> : null}
					</div>
					<ReferenceComponent />
				</div>
				</div>
			</MuiThemeProvider>
    	)
  	}
}

export default App;
