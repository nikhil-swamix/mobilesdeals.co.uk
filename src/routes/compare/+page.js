import * as helpers from '$lib/helpers.js';
import * as lib from '$lib';
let deals;

export async function load({ fetch, url }) {
	let filters = lib.qparse(url);
	let common_names = await lib.getjson('api/distinct/common_name', filters,fetch);
	common_names = await common_names;
	// if (Object.keys(filters).length >= 4 || filters['Telcos:device_product_json.product_type']) {
	// 	deals = await fetch('/api/find?' + lib.qstringify(filters));
	// 	deals = await deals.json();
	// }

	return { common_names };
}
