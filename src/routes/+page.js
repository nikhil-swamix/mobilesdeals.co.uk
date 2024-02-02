import * as lib from '$lib';
import { browser } from '$app/environment';
let response = [];


export async function load({ fetch, params, session }) {
	// Add your logic to fetch data here
	if (browser) {
		response = await lib.getjson('/api/distinct/merchant_name');
	}
	// >>> now for each of them we need to fetch logo_url
	let merchmap = {};

	for (let i = 0; i < response.length; i++) {
		merchmap[response[i]] =( await lib.getjson('api/distinct/Telcos:deal_retailer_json.logo_url', { merchant_name: response[i] }))[0];
		// console.log(merchmap[response[i]]);
	}

	return {
        merchants: merchmap,
    };
}
