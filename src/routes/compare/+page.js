import * as helpers from '$lib/helpers.js';
import * as lib from '$lib';
let deals;

export async function load({ fetch, url }) {

		let filters = lib.qparse(url);
		let common_names = await fetch('api/distinct/common_name?' + lib.qstringify(filters));
		common_names = await common_names.json();
		if (Object.keys(filters).length == 5) {
			deals = await fetch('/api/find?' + lib.qstringify(filters));
			deals = await deals.json();
		}


		return { common_names, deals };

}
