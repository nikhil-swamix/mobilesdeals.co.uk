import qs from 'query-string';
export { goto, afterNavigate, pushState, onNavigate, beforeNavigate, replaceState } from '$app/navigation';
export { page } from '$app/stores';
export { browser } from '$app/environment';

import axios from 'axios';

export const qparse = (url) => {
	let q = url?.search;
	return qs.parse(q);
};

// qstringify
export const qstringify = (obj) => {
	let q = qs.stringify(obj);
	return q;
};

// getjson
export const getjson = async (url, filters, _fetch = fetch) => {

	if (filters) {
		url = url + '?' + qstringify(filters);
	}
	let json = await _fetch(url).then((res) => res.json());
	// console.log(json);
	return json;
};
