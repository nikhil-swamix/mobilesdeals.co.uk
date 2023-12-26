import { connectDB } from '$lib/db';
import * as lib from '$lib';
import { mongoose } from 'mongoose';
import { json } from '@sveltejs/kit';
connectDB();

// create empty schema "MasterCatalog" with exact name
const MasterCatalog = mongoose.models.MasterCatalog || mongoose.model('MasterCatalog', {}, 'MasterCatalog');

export async function GET({ url, params, setHeaders }) {
	// console.log(url);
	// return 10 docs from the MasterCatalog
	if (params.path == 'find') {
		let findOpts = lib.qparse(url);
		let limit = findOpts.limit || 100;
		delete findOpts.limit;
		console.log(findOpts, limit);
		let docs = await MasterCatalog.find(findOpts).limit(limit);
		setHeaders({
			'Cache-Control': 'public,max-age=60'
		});
		return json(docs);
	}
	// add distinct path with this pattern /distinct/{key}?filter_conditions
	if (params.path.startsWith('distinct')) {
		let distinctor = params.path.split('/')[1];

		let t = new Date();
		let docs = await MasterCatalog.distinct(distinctor, lib.qparse(url));
		// let docs = ['await MasterCatalog.distinct(distinctor, filter)'];

		console.log('time taken: ', new Date() - t);
		// cache 1 hr
		setHeaders({
			'Cache-Control': 'public,max-age=3600'
		});
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
