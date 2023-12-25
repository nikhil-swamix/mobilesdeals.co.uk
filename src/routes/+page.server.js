export async function load({ params, fetch }) {
	// Replace with your API endpoint or local data fetching logic
	let data = await fetch(`https://jsonplaceholder.typicode.com/posts/${params.id}.json`).then((r) => r.json());
	return {
		data
	};
}
