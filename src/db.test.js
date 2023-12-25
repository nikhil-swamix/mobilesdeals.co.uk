import { Mongoose, Schema, Model } from 'mongoose';
// import dotenv
import dotenv from 'dotenv';
dotenv.config({ path: '../.env' });

// create a connection to the database
console.log(process.env.MONGO_URI);
const db = new Mongoose();

await db.connect(process.env.MONGO_URI);

// create schemaless model MasterCatalog
const MasterCatalog = db.model(
	'MasterCatalog',
	new Schema(
		{
			_id: String
		},
		{ collection: 'MasterCatalog' }
	)
);

// let result = await MasterCatalog.distinct('brand_name');
// let result = await MasterCatalog.distinct('Telcos:network');
let result = await MasterCatalog.distinct('Telcos:device_full_name');
for (let i = 0; i < result.length; i++) {
	console.log(result[i]);
}
// console.log(result);

process.exit(0);
