import React from 'react'
import Toggle from 'material-ui/Toggle';

export class ToggleGroup extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			tileName: false,
			basePairLocations: false,
			getVariants: false,
			getDiffIndices: false,
			indexInputError: false 
		}
	}

	render() {
		return (
			<div>
				<Toggle
					label="Get Tile Name" 
					labelPosition="right"
					onToggle={this.props.tileName}/>
				<Toggle
					label="Get Base Pair Locations" 
					labelPosition="right"
					onToggle={this.props.basePair}/>
				<Toggle
					label="Get Variants" 
					labelPosition="right"
					onToggle={this.props.variant}
					/>
				<Toggle 
					label="Get Diff Indices" 
					labelPosition="right"
					onToggle={this.props.diff}/>
			</div>
			)
	}
}