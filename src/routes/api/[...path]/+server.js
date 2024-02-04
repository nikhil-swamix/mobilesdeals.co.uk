import { connectDB } from '$lib/db';
import * as lib from '$lib';
import { mongoose } from 'mongoose';
import { json } from '@sveltejs/kit';
// npm i node-cache
import NodeCache from 'node-cache';

let cache = new NodeCache({ stdTTL: 3600, checkperiod: 3600 });
connectDB();

// create empty schema "MasterCatalog" with exact name
const MasterCatalog = mongoose.models.MasterCatalog || mongoose.model('MasterCatalog', {}, 'MasterCatalog');

export async function GET({ url, params, setHeaders }) {
	// console.log(url);
	let findOpts = lib.qparse(url);
	let limit = findOpts.limit || 200;
	let projections = findOpts?.projections || '{}';
	if (typeof projections == 'string') projections = JSON.parse(projections);
	delete findOpts.limit;
	delete findOpts.projections;
	if (params.path == 'find') {
		limit = limit !=1 && findOpts['Telcos:device_product_json.product_type'] == 'SIM Card' ? 1000 : limit;
		if (findOpts?.['Telcos:deal_type_json.deal_type_name'] == 'Consumer - Affiliate Price') {
			// let docs = await MasterCatalog.sample(20);
			let docs = await MasterCatalog.aggregate([
				{ $match: { 'Telcos:deal_type_json.deal_type_name': 'Consumer - Affiliate Price' } },
				{ $sample: { size: 20 } },
				
			]);
			console.log(findOpts);

			return json(docs);
		}
		let docs = await MasterCatalog.find(findOpts, projections).limit(limit);
		setHeaders({
			'Cache-Control': 'public,max-age=600'
		});
		return json(docs);
	}
	// add distinct path with this pattern /distinct/{key}?filter_conditions
	if (params.path.startsWith('distinct')) {
		// cache url
		let hash = url.pathname + url.search;
		let distinctor = params.path.split('/')[1];
		let t = new Date();
		let docs = cache.get(hash);
		// console.log(hash, docs?.length);
		setHeaders({
			'Cache-Control': 'public,max-age=3600'
		});
		if (docs) {
			// console.log('kashi memory',docs.length);
			return json(docs);
		} else {
			docs = await MasterCatalog.distinct(distinctor, lib.qparse(url));
			cache.set(hash, docs);
			console.log('time:' + url.search + distinctor, new Date() - t);
		}

		return json(docs);
	}
}

// create a post function to add data to the database
export async function POST({ request }) {
	let data = await request.formData();
	// insert data into the database
	console.log(data.get('name'));
	return new Response(data);
}
