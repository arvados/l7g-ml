import Axios from 'axios'

const tileIpAddress = 'http://192.168.1.156:8080'

export async function callApi(searchObject, callback) { 
	try {
		var response = await Axios.get(`${tileIpAddress}/tile?
		index=${searchObject.index}
		&get_base_locs=${searchObject.getBasePairLocations}
		&get_variants=${searchObject.getVariants}
		&get_name=${searchObject.getTileName}
		&get_diff_indices=${searchObject.getDiffIndices}
		&json=true`, {
			headers: {
				'Content-Type': 'text/json'
				}
		})
		callback(response.data, null)
	} catch(error) {
			alert(error)
			console.log(error)
			callback(null, error)
	}
}
