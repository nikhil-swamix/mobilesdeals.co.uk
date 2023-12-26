import qs from 'query-string';
export { goto } from '$app/navigation';
export { page } from '$app/stores';
export const qparse = (url) => {
	let q = url?.search;
	return qs.parse(q);
};

// qstringify
export const qstringify = (obj) => {
    let q = qs.stringify(obj);
    return q;
}

// getjson
export const getjson = async (url,filters) => {
    if(filters){
        url = url + '?' + qstringify(filters);
    }
    let res = await fetch(url);
    let json = await res.json();
    return json;
}