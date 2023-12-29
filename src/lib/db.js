import mongoose from 'mongoose';
import { MONGO_URI } from '$env/static/private';
// import Models from './models.js';
// console.log(MONGO_URI);

export const connectDB = async () => {
	try {
		const conn = await mongoose.connect(MONGO_URI, {});

		console.log(`MongoDB Connected: ${conn.connection.host}`);
	} catch (error) {
		console.error(`Error: ${error.message}`);
		// exit with failure
		process.exit(1);
	}
};
