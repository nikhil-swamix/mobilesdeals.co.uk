<script>
	// export let data;
	import { browser } from '$app/environment';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import * as lib from '$lib';
	import * as helpers from '$lib/helpers';
	import ProductModelCard from './ProductModelCard.svelte';
	import Dtable from './Dtable.svelte';
	import sf from '$lib/stores/shadowFilters';

	let shadowFilters = { ...$sf, ...lib.qparse($page.url) };
	if (shadowFilters.common_name && shadowFilters.common_name.includes('  ')) {
		shadowFilters.common_name = shadowFilters.common_name.replace('  ', '+ ');
	}

	let deals = [];
	let table;
	let common_names = [];
	/* 	setInterval(() => { if (JSON.stringify(shadowFilters) != JSON.stringify(lib.qparse($page.url))) { lib.replaceState(`/compare?${lib.qstringify(shadowFilters)}`, $page.state); console.log(lib.qparse($page.url), shadowFilters); } }, 200); */
	$: {
		if (Object.keys($sf).length != 1) {
			shadowFilters = purify({ ...lib.qparse($page.url), ...$sf });
		} else {
			shadowFilters = $sf;
		}
		console.log(shadowFilters);

		// console.log(Object.keys($sf).length != Object.keys(lib.qparse($page.url)).length);
		if (Object.keys($sf).length != Object.keys(lib.qparse($page.url)).length) {
			try {
				lib.browser && lib.replaceState(`/compare?${lib.qstringify(shadowFilters)}`, $page.state);
				shadowFilters = { ...$sf, ...lib.qparse($page.url), ...shadowFilters };
			} catch (error) {}
			console.log(lib.qparse($page.url), shadowFilters);
		}
		$sf = shadowFilters;

		browser && lib.getjson('/api/distinct/common_name', shadowFilters).then((x) => (common_names = x));
	}

	function niggate(obj, delkey) {
		let robj = {};
		for (const key in obj) {
			if (key != delkey) {
				robj[key] = obj[key];
			}
		}
		return robj;
	}
	function purify(obj) {
		return Object.fromEntries(Object.entries(obj).filter(([k, v]) => v != null));
	}

	async function updateDeals() {
		let projections = {
			'Telcos:deal_retailer_json.logo_url': 1,
			'Telcos:initial_cost': 1,
			'Telcos:deal_cost_json': 1,
			'Telcos:month_cost': 1,
			'Telcos:term': 1,
			'Telcos:inc_minutes': 1,
			'Telcos:inc_texts': 1,
			'Telcos:connectivity': 1,
			'Telcos:tariff': 1,
			_id: 1,
			'Telcos:deal_type_json.deal_type_name': 1
		};
		projections = JSON.stringify(projections);
		deals = await lib.getjson('/api/find', { ...shadowFilters, projections });
		setTimeout(() => {
			if (table) {
				table = undefined;
			}
		}, 200);

		return deals;
	}
	onMount(async () => {
		common_names = await lib.getjson('/api/distinct/common_name', shadowFilters);
		// console.log(shadowFilters, common_names);
	});
	onDestroy(async () => {
		sf.set({});
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" />
</svelte:head>
<div class="row p-lg-2 mx-lg-5 mx-0">
	{#key shadowFilters}
		<div class="btn-group w-auto" role="group">
			<div class="btn btn-{!shadowFilters['Telcos:network'] ? 'danger blink' : 'success'}">
				<i class="fas fa-diagram-project" />
				Network
			</div>

			{#await lib.getjson('/api/distinct/Telcos:network', shadowFilters)}
				<button class="btn btn-primary" type="button" disabled>
					<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
					Loading...
				</button>
			{:then data}
				{#each data as m}
					<button
						type="button"
						class="btn btn-outline-dark {shadowFilters['Telcos:network'] == m ? 'active' : ''}"
						on:click={() => {
							shadowFilters['Telcos:network'] = m;
						}}
					>
						{m}
					</button>
				{/each}

				<button
					class="btn btn-danger"
					on:click={() => {
						$sf = niggate(shadowFilters, 'Telcos:network');
						shadowFilters['Telcos:network'] = undefined;
					}}
				>
					<i class="fas fa-times" />
				</button>
			{/await}
		</div>
		<div class="btn-group w-auto" role="group">
			<div class="btn btn-{!shadowFilters['merchant_name'] ? 'danger blink' : 'success'}">
				<i class="fas fa-shop" />
				Merchant
			</div>

			{#await lib.getjson('/api/distinct/merchant_name', shadowFilters)}
				<button class="btn btn-primary" type="button" disabled>
					<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
					Loading...
				</button>
			{:then data}
				{#each data as m}
					<button
						type="button"
						class="btn btn-outline-dark {shadowFilters['merchant_name'] == m ? 'active' : ''}"
						on:click={() => {
							shadowFilters['merchant_name'] = m;
							// delete shadowFilters['Telcos:network'];
						}}
					>
						{m}
					</button>
				{/each}
				<button
					class="btn btn-danger"
					on:click={async () => {
						$sf = niggate(shadowFilters, 'merchant_name');
						shadowFilters['merchant_name'] = undefined;
						await goto(`/compare?${lib.qstringify(niggate(shadowFilters, 'merchant_name'))}`);
					}}
				>
					<i class="fas fa-times" />
				</button>
			{/await}
		</div>

		<!-- {#key shadowFilters.colour} -->
		<div>
			<div class="btn-group mt-2 w-auto" role="group" aria-label="Button group name">
				{#await lib.getjson('/api/distinct/colour', niggate(shadowFilters, 'colour'))}
					<!-- promise is pending -->
				{:then colours}
					<button type="button" class="btn btn-primary btn-sm fw-bold"> Select Colour </button>

					{#each colours as colour}
						<button
							class="btn btn-{shadowFilters['colour'] == colour ? 'dark' : 'light'} bg-gradient"
							on:click={() => {
								shadowFilters.colour = colour;
							}}
						>
							<i class="fas fa-circle fa-lg shadow" style="color: {helpers.colormap[colour]}; text-shadow: 0 0 1px black;" />
							{colour}
						</button>
					{/each}
				{/await}
			</div>
		</div>
		<!-- {/key} -->
		{#key shadowFilters['Telcos:storage_size']}
			<div class="btn-group mt-2 w-auto" role="group" aria-label="Button group name">
				{#await lib.getjson('/api/distinct/Telcos:storage_size', niggate(shadowFilters, 'Telcos:storage_size'))}
					<button class="btn btn-primary" type="button" disabled>
						<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
						Loading...
					</button>
				{:then sz}
					<button type="button" class="btn btn-primary btn-sm fw-bold"> Storage </button>

					{#each sz as s}
						<button
							class="btn btn-{shadowFilters['Telcos:storage_size'] == s ? 'dark' : 'light'}  "
							on:click={() => {
								shadowFilters['Telcos:storage_size'] = s;
							}}
						>
							{s}
						</button>
					{/each}
				{/await}
			</div>
		{/key}

		<!-- ------------------------------ -->
		<div class="col-12 row mt-2 mt-lg-2 px-4" id="filters">
			{#if shadowFilters && Object.keys(shadowFilters).length > 0}
				<div class="col-auto py-1 d-flex align-items-center btn btn-dark me-2">
					<!-- fa tick -->
					<i class="fas fa-check-circle text-success me-2" />
					My Selections
				</div>
				{#each Object.entries(shadowFilters) as [key, value] (key)}
					<!-- create a button group -->
					{#if key !== 'Telcos:network' && key !== 'merchant_name'}
						<div class="btn-group col-auto btn-group-sm px-0 me-lg-2 shadow">
							<button type="button" class="btn py-0 px-1 btn-primary">{helpers.attrTranslate[key]}</button>
							<button type="button" class="btn py-0 px-1 btn-outline-dark">{value}</button>
							<button
								type="button"
								class="btn py-0 px-1 btn-danger"
								on:click={async () => {
									delete shadowFilters[key];
									await goto(`/compare?${lib.qstringify(shadowFilters)}`);
									window.location.reload();
								}}><i class="fas fa-times" /></button
							>
						</div>
					{/if}
				{/each}
				{#if !shadowFilters?.common_name}
					<button type="button" class="btn btn-warning btn-sm col-auto me-2 blink">Please select a Model</button>
				{/if}
				{#if !shadowFilters?.colour}
					<button type="button" class="btn btn-warning btn-sm col-auto me-2 blink">Please select a Colour</button>
				{/if}
				{#if !shadowFilters['Telcos:storage_size']}
					<button type="button" class="btn btn-warning btn-sm col-auto me-2 blink">Please select a Storage</button>
				{/if}
				<!-- <button class="btn btn-danger btn-sm" on:click={() => (filters = {})}>Clear</button> -->
			{:else}{/if}
		</div>
	{/key}
	{#if Object.keys(shadowFilters).length >= 1}
		<div class="row col-12 ps-3 ps-lg-0 mx-auto my-lg-3">
			{#if shadowFilters?.common_name}
				<ProductModelCard cname={shadowFilters.common_name} />
			{:else if common_names.length > 0}
				{#each common_names as cname}
					<ProductModelCard {cname} />
				{/each}
			{/if}
		</div>
	{:else}
		<p class="lead text-danger m-0 mt-3">Please Select Few More Filters</p>
	{/if}
	{#key shadowFilters}
		{#if (shadowFilters?.common_name && shadowFilters?.colour && shadowFilters['Telcos:storage_size']) || shadowFilters['Telcos:device_product_json.product_type'] === 'SIM Card'}
			<h2 class="display-4 fw-bold">Available Deals</h2>
			{#await updateDeals() then x}
				{#if deals.length > 0}
					<Dtable {deals} />
				{/if}
			{/await}

			<!-- content here -->
		{/if}
	{/key}
</div>

<!-- 

	deal schema
	[
		{
			"_id": "6574166d981a5e3efc0c4b92",
			"product_name": "Apple iPhone 12 5G (64GB White) at £30 on Lite 2GB (36 Month contract) with Unlimited mins & texts; 2GB of 5G data. £26 a month.",
        "common_name": "Apple iPhone 12 5G",
        "colour": "White",
        "brand_name": "Apple",
        "aw_deep_link": "https://www.awin1.com/pclick.php?p=36286963872&a=123501&m=10210",
        "merchant_name": "Three",
        "merchant_category": "Mobile Phone - PAYM",
        "merchant_image_url": "https://media.bigupdata.co.uk/2022-02-01_15-06-29_img_product_image_main_large1_reseller_product_edition0000271483.png?h=400&w=400&auto=enhance&auto=format&bg=FFFFFF&trim=color&trimcolor=FFFFFF&trim=auto&trimtol=2",
        "merchant_thumb_url": "https://media.bigupdata.co.uk/2022-02-01_15-06-29_img_product_image_main_large1_reseller_product_edition0000271483.png?h=150&w=150&auto=enhance&auto=format&bg=FFFFFF&trim=color&trimcolor=FFFFFF&trim=auto&trimtol=2",
        "description": "iPhone 12 has superfast 5G, A14 Bionic, the fastest chip in a smartphone, 6.1-inch display built with Gorilla Glass and an aluminium frame. The scratch resistant glass with oleophobic coating also provides extra protection. The Super Retina XDR display and a camera system that takes low-light photography to the next level. The sound is also high quality with stereo speakers.",
        "Telcos:device_full_name": "Apple iPhone 12 5G (64GB White)",
        "Telcos:network": "Three",
        "Telcos:gift": null,
        "Telcos:device_product_json": {
            "product_type": "Mobile Phone",
            "product_id": "1",
            "product_brand": "Apple",
            "product_brand_id": "4",
            "product_name": "iPhone",
            "product_type_id": "1"
        },
        "Telcos:device_product_version_json": {
            "product_version_name": "12 5G",
            "product_version_id": "54521"
        },
        "Telcos:initial_cost": 30,
        "Telcos:month_cost": 26,
        "Telcos:tariff": "Lite 2GB",
        "Telcos:inc_minutes": "Unlimited",
        "Telcos:inc_texts": "Unlimited",
        "Telcos:connectivity": "5G",
        "Telcos:inc_data": "2000",
        "Telcos:storage_size": "64GB",
        "Telcos:deal_retailer_json": {
            "logo_url": "https://media.bigupdata.co.uk/img_company_logo_large1_company0000000036.png",
            "company_id": "36",
            "terms_url": "http://www.three.co.uk/terms-conditions",
            "name": "Three"
        },
        "Telcos:deal_type_json": {
            "deal_type_name": "Consumer",
            "deal_type_id": "0"
        },
        "Telcos:deal_cost_json": {
            "tco_inc_vat": "966.00",
            "monthly_device_final_term_exc_vat": "",
            "upfront_inc_vat": "30.00",
            "monthly_total_previous_inc_vat": "28.75",
            "tco_exc_vat": "805.00",
            "ecpm_inc_vat": "26.83",
            "monthly_device_final_term_months": "",
            "ecpm_exc_vat": "22.36",
            "upfront_exc_vat": "25.00",
            "monthly_device_term_months": "36",
            "monthly_device_final_term_inc_vat": "",
            "monthly_contract_term_months": "24",
            "monthly_total_inc_vat": "26.00",
            "monthly_device_inc_vat": "13.00",
            "upfront_previous_inc_vat": "",
            "monthly_contract_inc_vat": "13.00",
            "upfront_previous_exc_vat": "",
            "monthly_contract_exc_vat": "10.83",
            "monthly_device_exc_vat": "10.83",
            "monthly_total_exc_vat": "21.67",
            "monthly_total_previous_exc_vat": "23.96"
        },
        "data_feed_id": 18901
    }
]

 -->

<style>
	.btn-group * {
		/* font-weight: 600; */
	}
	.btn-group {
		min-width: 8em;
	}
	@media (min-width: 768px) {
		.mw-lg-12em {
			min-width: 12em !important;
		}
	}
	@media (max-width: 768px) {
		.btn-group * {
			font-size: 0.8em;
		}
	}

	.blink {
		animation: blinker 1.5s linear infinite;
	}
	@keyframes blinker {
		50% {
			opacity: 0;
		}
	}
</style>
