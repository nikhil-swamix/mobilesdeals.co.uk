<script>
	export let data;
	import { onMount } from 'svelte';
	import * as lib from '$lib';
	import * as helpers from '$lib/helpers';
	import ProductModelCard from './ProductModelCard.svelte';
	import { browser } from '$app/environment';
	let page = lib.page;
	let filters = lib.qparse($page.url);
	let shadowFilters = filters;
	$: {
		// shadowFilters = { ...shadowFilters };
		if (browser) lib.goto('?' + lib.qstringify(shadowFilters));
	}
	onMount(() => {
		console.log($page.state);
	});
	lib.afterNavigate(() => {
		// if (browser) lib.pushState('?' + lib.qstringify(shadowFilters));
		console.log('trig url params updates');
		// if (lib.qparse($page.url) !== shadowFilters) {
		// }
		// lib.goto('?' + lib.qstringify(shadowFilters));
		// window.location.href = "?" + lib.qstringify(shadowFilters);
		console.log('Navigation Event', shadowFilters);
	});
</script>

<div class="row p-lg-4 mx-lg-5 mx-0">
	<div class="col-12 row mt-2 mt-lg-2" id="filters">
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
					<!-- add fa x -->
					<button type="button" class="btn py-0 px-1 btn-danger" on:click={() => delete shadowFilters[key] && (shadowFilters = shadowFilters)}><i class="fas fa-times" /></button>
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
		{#key $page.url}
			<!-- <ProductModelCard cname={shadowFilters.common_name} bind:shadowFilters /> -->

			{#each data.common_names as cname}
				<ProductModelCard {cname} filters={{ ...filters }} bind:shadowFilters />
			{/each}
		{/key}
	</div>

	{#if Object.keys(shadowFilters).length == 5}
		<h2 class="display-4 fw-bold">Available Deals</h2>

		<div class="row col-12 p-0 ps-lg-0 mx-lg-auto mx-0 px-0">
			{#await helpers.getDeals({ ...shadowFilters }) then value}
				{#each value as deal}
					<!-- DISPLAY INSTRUCTIONS ; card horizontal, col1 = [Telcos:deal_retailer_json.[name,logourl]] col2 = [price] col2 [monthly, total cost] -->
					<div class=" col-lg-12 col-12 px-0 py-2 border-top">
						<div class="row mx-0 d-flex justify-content-start align-items-center">
							<div class="col-lg-1 col-3 d-flex align-items-center p-1">
								<img src={deal['Telcos:deal_retailer_json']['logo_url']} class="card-img img-fluid" alt="..." />
							</div>
							<!-- monthly -->
							<div class=" col-auto col-lg-auto px-0 pt-lg-0">
								<div class="btn-group" role="group">
									<button type="button" class="btn btn-dark px-2">
										<i class="fa-duotone fa-pound-sign" />
										Monthly
									</button>
									<button type="button" class="btn btn-outline-dark fw-bold">{deal['Telcos:deal_cost_json']['monthly_total_inc_vat']} </button>
								</div>
							</div>
							<div class=" col-auto col-lg-auto px-0 ps-lg-2 pt-lg-0">
								<div class="btn-group mw-lg-12em row mx-0" role="group">
									<button type="button" class="btn btn-dark fw-normal col-auto">
										<i class="fa-duotone fa-pound-sign px-0" />
										Upfront
									</button>
									<button type="button" class="btn btn-outline-dark text-center fw-bold col-3 p-0">{Math.round(deal['Telcos:initial_cost'])} </button>
								</div>
							</div>
							<div class=" col-3 col-lg-auto px-1 pt-2 pt-lg-0">
								<div class="btn-group btn-group-sm" role="group">
									<button type="button" class="btn btn-dark fw-normal px-0">
										Total
										<!-- <i class="fa-duotone fa-fw fa-pound-sign" /> -->
									</button>
									<button type="button" class="btn btn-outline-dark text-center">{deal['Telcos:deal_cost_json']['tco_inc_vat']} </button>
								</div>
							</div>
							<div class=" col-3 col-lg-auto px-1 pt-2 pt-lg-0">
								<div class="btn-group btn-group-sm" role="group">
									<button type="button" class="btn btn-dark fw-normal px-0" title="contract Duration">
										<i class="fa-duotone fa-fw fa-timer" />
									</button>
									<button type="button" class="btn btn-outline-dark">{deal['Telcos:deal_cost_json']['monthly_contract_term_months']} Months</button>
								</div>
							</div>
							<div class=" col-6 col-lg-auto px-1 pt-2 pt-lg-0">
								<div class="btn-group btn-group-sm" role="group">
									<button type="button" class="btn btn-dark fw-normal" title="Talktime minutes">
										<i class="fa-duotone fa-fw fa-phone-arrow-down" />
									</button>
									<button type="button" class="btn btn-outline-dark text-success">{deal['Telcos:inc_minutes']}</button>
									<button type="button" class="btn btn-dark fw-normal">
										<i class="fa-duotone fa-fw fa-sms" />
									</button>
									<button type="button" class="btn btn-outline-dark text-success">
										{deal['Telcos:inc_texts']}
									</button>
								</div>
							</div>
							<div class=" col-6 col-lg-2 px-1 pt-2 pt-lg-0">
								<div class="row mx-0 btn-group btn-group-sm col-12" role="group">
									<button type="button" class="btn col-lg-2 btn-dark fw-normal" title="Data">
										<i class="fa-duotone fa-arrow-up-arrow-down" />
									</button>
									<button type="button" class="btn col-lg-2 bg-opacity-25 bg-dark fw-normal">
										{deal['Telcos:connectivity'].replace(/ /g, '')}
									</button>
									<button type="button" class="btn col-lg-6 btn-outline-dark">
										{deal['Telcos:tariff'].split(' ').slice(1).join(' ')}
									</button>
								</div>
							</div>
							<div class=" col-6 col-lg-2 px-1 pt-2 pt-lg-0">
								<a class="btn btn-lg btn-success" href="deal?_id={deal._id}" target="_blank">
									View Deal
									<i class="fa-duotone fa-cart-shopping-fast" />
								</a>
							</div>
						</div>
					</div>
				{/each}
			{/await}
		</div>
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
</style>
