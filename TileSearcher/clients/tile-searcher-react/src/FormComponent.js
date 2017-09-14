import React from 'react'
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import { ToggleGroup } from "./ToggleMaterial"

const style = {
	padding: 16
}

const submitButtonStyle ={
	marginTop: 16,
	textAlign: 'center'
}

export class FormComponent extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			index: '',
			loading: false,
			getTileName: false,
			getBasePairLocations: false,
			getVariants: false,
			getDiffIndices: false,
			indexInputError: false 
		}
		this.handleSubmit = this.handleSubmit.bind(this)
		this.handleIndexChange = this.handleIndexChange.bind(this)

		this.handleTileNameToggle = this.handleTileNameToggle.bind(this)
		this.handleBasePairToggle = this.handleBasePairToggle.bind(this)
		this.handleVariantToggle = this.handleVariantToggle.bind(this)
		this.handleDiffToggle = this.handleDiffToggle.bind(this)
	}

	handleTileNameToggle() {
		this.setState({
			getTileName: !this.state.getTileName
		})
	}

	handleBasePairToggle() {
		this.setState({getBasePairLocations: !this.state.getBasePairLocations})
	}

	handleVariantToggle() {
		this.setState({getVariants: !this.state.getVariants})
	}


	handleDiffToggle() {
		this.setState({getDiffIndices: !this.state.getDiffIndices})
	}

	handleSubmit() {
		var searchObject = {
			index: this.state.index,
			getTileName: this.state.getTileName,
			getBasePairLocations: this.state.getBasePairLocations,
			getVariants: this.state.getVariants,
			getDiffIndices: this.state.getDiffIndices
		}
		this.props.setLoading(true)
		this.props.onSubmit(searchObject, (err) => this.props.setLoading(false))
	}

	handleIndexChange(e) {
		if (typeof e.target.value !== 'number') {
			this.setState({
				indexInputError: true
			})
		} else {
			this.setState({
				indexInputError: false
			})
		}
		this.setState({
			[e.target.name]: e.target.value
		})
	}

	render() {
		return (
			<div style={style} >
				<b>Input values for tile search</b><br/>
				<TextField floatingLabelText="Index"
				 	name="index"
				 	errorText={() => {
				 		if (this.state.indexInputError) {
				 			return "Index must be a number"
				 		} else {
				 			return null
				 		}
				 	}}
				 	onSubmit={this.handleSubmit}
				 	onChange={this.handleIndexChange}/><br/>
				 <ToggleGroup tileName={this.handleTileNameToggle}
				 	basePair={this.handleBasePairToggle}
				 	diff={this.handleDiffToggle}
				 	variant={this.handleVariantToggle}
				 	/>
				
				<RaisedButton label='search' 
					backgroundColor="#303f9f"
					labelColor="#ffffff"
					style={submitButtonStyle}
					onClick={this.handleSubmit}/><br/><br/><br/>


			</div>
		);
	}	
}