<script>
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import * as lib from '$lib';
	import * as helpers from '$lib/helpers';
	let affiliateDeals = [];
	function calcDataSort(deal) {
		// deal['Telcos:tariff'] has integers and sometimes unlimited, we need to assign 999 to unlimited and integer to integer
		// try using regex and parseint
		let is_unlimited = deal['Telcos:tariff'].toLowerCase().includes('unlimited');
		let int = parseInt(deal['Telcos:tariff'].replace(/[^0-9]/g, ''));
		// console.log(deal['Telcos:tariff'], is_unlimited, int);
		if (is_unlimited) {
			return "Unltd";
		} else if (int) {
			return int;
		} else {
			return 0;
		}
	}
	onMount(async () => {
		affiliateDeals = await lib.getjson('/api/find', { 'Telcos:deal_type_json.deal_type_name': 'Consumer - Affiliate Price' });
	});
</script>

<h2 class="fw-bold text-center my-5">
	Special Deals

	<button
		type="button"
		class="btn btn-primary"
		on:click={async () => {
			// affiliateDeals = [];
			affiliateDeals = await lib.getjson('/api/find', { 'Telcos:deal_type_json.deal_type_name': 'Consumer - Affiliate Price' });
		}}
	>
		<i class="fa-duotone fa-sync"></i> Reload
	</button>
</h2>
<div class="row justify-content-center">
	{#each affiliateDeals as d}
		<div class="card col-2 px-0 text-center mb-3 me-3 shadow border-0">
			<h4 class="lead bg-dark text-white rounded-top-2 d-flex align-items-center justify-content-center px-2">{d['common_name']}</h4>
			<div>
				<a class="" href="deal?_id={d._id}" target="_blank">
					<img class="img-fluid" src={d.merchant_thumb_url} alt="Card image cap" />
				</a>
			</div>
			<div class="btn-group btn-group-sm mt-2 mx-2" role="group" aria-label="Button group name">
				<button type="button" class="btn px-1 btn-outline-dark fw-bold">£{d['Telcos:month_cost']} for {d['Telcos:term']} Mo</button>
				<button type="button" class="btn px-1 btn-outline-dark">£{d['Telcos:initial_cost']} Upfront</button>
				<!-- <button type="button" class="btn btn-outline-dark"> Third One </button> -->
			</div>
			<div class=" btn-group p-2 pt-1">
				<button type="button" class="btn btn-sm btn-outline-dark me-1 py-0">{d['Telcos:storage_size']}</button>
				<button type="button" class="btn btn-sm btn-outline-dark me-1 py-0 {d['colour'] == 'White' ? '' : 'text-white'}" style="background-color: {helpers.colormap[d['colour']]};">
					{d['colour']}
				</button>
				<button type="button" class="btn btn-sm btn-outline-dark  py-0">
                    <i class="fa-duotone fa-arrow-up-arrow-down"></i>
                    {calcDataSort(d)} GB</button>
			</div>
		</div>
	{/each}
</div>

<!-- {JSON.stringify(affiliateDeals)} -->

<style>
	img {
		max-width: 12em;
		height: 12em;
		/* width: auto; */
	}
	h4 {
		min-height: 2.2em;
		line-height: 1em;
	}
</style>
