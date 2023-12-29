import * as helpers from '$lib/helpers.js';
import * as lib from '$lib';

export async function load({fetch,url}) {
    let filters = lib.qparse(url);
    let common_names = await fetch('api/distinct/common_name?' + lib.qstringify(filters));
    common_names = await common_names.json();
    console.log(filters,common_names);

	return { common_names };
}
