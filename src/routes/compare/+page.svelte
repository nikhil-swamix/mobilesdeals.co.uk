<script>
	export let data;
	import { onMount, onDestroy } from 'svelte';
	import * as lib from '$lib';
	import * as helpers from '$lib/helpers';
	import ProductModelCard from './ProductModelCard.svelte';
	import { browser } from '$app/environment';
	import DataTable from 'datatables.net-bs5';
	// import 'datatables.net-buttons-bs5';
	// import 'datatables.net-responsive-bs5';
	import { goto } from '$app/navigation';

	
	let timer;
	let page = lib.page;
	let shadowFilters = lib.qparse($page.url);

	setInterval(() => {
		if (JSON.stringify(shadowFilters) != JSON.stringify(lib.qparse($page.url))) {
			// shadowFilters = lib.qparse($page.url);
			goto(`/compare?${lib.qstringify(shadowFilters)}`);
			// console.log(lib.qparse($page.url),shadowFilters);
		}
	}, 200);
	onMount(() => {
		let table = new DataTable('#myTable', {
			autoWidth: true
		});
		console.log(data);
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" />
</svelte:head>
<div class="row p-lg-2 mx-lg-5 mx-0">
	{#if !shadowFilters['merchant_name']}
		<p class="lead text-danger m-0">Please Select Merchant</p>
		<div class="btn-group" role="group" aria-label="Button group name">
			{#await lib.getjson('/api/distinct/merchant_name', shadowFilters) then data}
				{#each data as m}
					<button type="button" class="btn btn-outline-primary {shadowFilters['merchant_name'] == m ? 'active' : ''}" on:click={() => (shadowFilters['merchant_name'] = m)}>
						{m}
					</button>
				{/each}
			{/await}
		</div>
	{:else}
		<div class="btn-group btn-group" role="group" aria-label="">
			<button type="button" class="btn btn-dark "> Merchant </button>

			<button type="button" class="btn btn-primary" autocomplete="off">
				{shadowFilters['merchant_name']}
			</button>
		</div>
	{/if}
	{#if !shadowFilters['Telcos:network']}
		<p class="lead text-danger m-0 mt-3">Please Select Network</p>
		<div class="btn-group" role="group" aria-label="Button group name">
			{#await lib.getjson('/api/distinct/Telcos:network', shadowFilters) then data}
				{#each data as m}
					<button type="button" class="btn btn-outline-primary {shadowFilters['Telcos:network'] == m ? 'active' : ''}" on:click={() => (shadowFilters['Telcos:network'] = m)}>
						{m}
					</button>
				{/each}
			{/await}
		</div>
	{:else}
		<div class="btn-group btn-group mt-3" role="group" aria-label="">
			<button type="button" class="btn btn-dark "> Merchant </button>

			<button type="button" class="btn btn-primary" autocomplete="off">
				{shadowFilters['Telcos:network']}
			</button>
		</div>
	{/if}
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
			{/each}
			{#if !shadowFilters?.common_name}
				<button type="button" class="btn btn-warning btn-sm col-auto me-2">Please select a Model</button>
			{/if}
			{#if !shadowFilters?.colour}
				<button type="button" class="btn btn-warning btn-sm col-auto me-2">Please select a Colour</button>
			{/if}
			{#if !shadowFilters['Telcos:storage_size']}
				<button type="button" class="btn btn-warning btn-sm col-auto me-2">Please select a Storage</button>
			{/if}
			<!-- <button class="btn btn-danger btn-sm" on:click={() => (filters = {})}>Clear</button> -->
		{:else}
			Please select a network and brand to start comparing
		{/if}
	</div>
	<div class="row col-12 ps-3 ps-lg-0 mx-auto my-lg-3">
		{#each data.common_names as cname}
			<ProductModelCard {cname} bind:shadowFilters />
		{/each}
	</div>

	{#if data.deals}
		<h2 class="display-4 fw-bold">Available Deals</h2>

		<table class="table fixed" id="myTable">
			<thead>
				<tr>
					<th class="m-0 p-0 h5">Retailer</th>
					<th class="m-0 p-0 h5"> Monthly </th>
					<th class="m-0 p-0 h5">Upfront</th>
					<th class="m-0 p-0 h5">Total</th>
					<th class="m-0 p-0 h5">Contract Duration</th>
					<th class="m-0 p-0 h5">Traiff</th>
					<th class="m-0 p-0 h5">Data</th>
					<th class="m-0 p-0 h5">View Deal</th>
				</tr>
			</thead>
			<tbody>
				{#each data.deals as deal}
					<tr class="">
						<td class="col">
							<img src={deal['Telcos:deal_retailer_json']['logo_url']} class="img-fluid" alt="..." />
						</td>
						<td class="">
							<button type="button" class="btn btn-outline-dark btn-sm fw-bold">
								<i class="fa-duotone fa-pound-sign"></i>
								{deal['Telcos:deal_cost_json']['monthly_total_inc_vat']}
							</button>
						</td>
						<td class="px-0">
							<i class="fa-duotone fa-pound-sign"></i>
							{deal['Telcos:initial_cost']}
						</td>
						<td class="px-0">
							<button type="button" class="btn btn-outline-dark btn-sm fw-bold">
								<i class="fa-duotone fa-pound-sign"></i>
								{deal['Telcos:deal_cost_json']['tco_inc_vat']}
							</button>
						</td>
						<td class="px-0">
							<div class="btn-group btn-group-sm" role="group">
								<button type="button" class="btn btn-dark fw-normal px-0" title="Contract Duration">
									<i class="fa-duotone fa-fw fa-timer"></i>
								</button>
								<button type="button" class="btn btn-outline-dark">
									{deal['Telcos:deal_cost_json']['monthly_contract_term_months']} Mo
								</button>
							</div>
						</td>
						<td class="px-0">
							<div class="btn-group btn-group-sm" role="group">
								<button type="button" class="btn btn-dark fw-normal" title="Talktime minutes">
									<i class="fa-duotone fa-fw fa-phone-arrow-down"></i>
								</button>
								<button type="button" class="btn btn-outline-dark">
									{deal['Telcos:inc_minutes'] == 'Unlimited' ? 'Unltd.' : `${deal['Telcos:inc_minutes']}`}
								</button>
								<button type="button" class="btn btn-dark fw-normal">
									<i class="fa-duotone fa-fw fa-sms"></i>
								</button>
								<button type="button" class="btn btn-outline-dark">
									{deal['Telcos:inc_texts']}
								</button>
							</div>
						</td>
						<td class="px-0">
							<div class="btn-group btn-group-sm" role="group">
								<button type="button" class="btn btn-dark fw-normal">
									{deal['Telcos:connectivity'].replace(/ /g, '')}
								</button>
								<button type="button" class="btn btn-outline-dark">
									{deal['Telcos:tariff']}
								</button>
							</div>
						</td>
						<td class="px-0">
							<a class="btn btn-success" href="deal?_id={deal._id}" target="_blank">
								View Deal <i class="fa-duotone fa-cart-shopping-fast"></i>
							</a>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
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
		font-weight: 600;
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
	.card-img {
		max-height: 4em;
		width: auto;
		margin: auto;
	}
	table img {
		max-height: 3em;
	}
</style>
