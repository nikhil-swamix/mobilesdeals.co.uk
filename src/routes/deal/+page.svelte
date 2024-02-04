<script>
	import { onMount } from 'svelte';
	import * as lib from '$lib';
	let deal;
	let page = lib.page;
	let filters = lib.qparse($page.url);
	onMount(async () => {
		const response = await lib.getjson(`/api/find?${lib.qstringify(filters)}`); // Replace `/api/deals/${id}` with your API endpoint to fetch the deal document
		console.log(filters);
		console.log(response);
		deal = response[0];
	});
</script>

<div class="container pt-5 min-vh-100">
	{#if deal}
		<div class="row d-flex justify-content-center align-items-center">
			<div class="col-12 col-lg-3 text-center py-3">
				<div class="deal-image">
					<img src={deal.merchant_image_url} alt={deal.common_name} />
				</div>
			</div>
			<div class="row col-12 col-lg-9">
				<h2>
					{deal.product_name.replace('(Consumer - Affiliate Price)', '')}
				</h2>
				<div class="deal-description">
					<p>{deal.description}</p>
				</div>
				<div class="col-lg-12 text-center btn btn-success p-lg-3 mt-lg-5">
					Buy Now
				</div>
			</div>
		</div>
	{:else}
		<h2 class="text-center display-1">Loading...</h2>
	{/if}
</div>

<style>
	.deal-container {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		/* Add any additional styling for the container */
	}

	.deal-image {
		flex: 1;
		/* Add any additional styling for the image */
	}

	.deal-image img {
		max-width: 100%;
		height: auto;
	}

	.deal-description {
		flex: 1;
		/* Add any additional styling for the description */
	}
</style>
