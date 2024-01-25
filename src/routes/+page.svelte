<script>
	import { onMount } from 'svelte';
	import * as lib from '$lib';
	import { getCommonNames, getDistinctBrands, getDistinctTelcos, colormap, getDistinctSimProviders } from '$lib/helpers';
	export let data;

	let commonNames = [];
	let filteredResults = [];
	let searchTerm = '';
	let selections = {};



	async function getDistinctColours() {
		// remove null
		return (await lib.getjson('api/distinct/colour?' + lib.qstringify(selections))).filter((c) => c != null);
	}
	// Telcos:storage_size
	async function getDistinctSizes() {
		return await lib.getjson('api/distinct/Telcos:storage_size?' + lib.qstringify(selections));
	}

	async function getDistinctBroadbandModels(ptype = 'Mobile Wi-Fi') {
		let items = await lib.getjson('api/distinct/common_name?Telcos:device_product_json.product_type=Mobile Wi-Fi' + lib.qstringify(selections));
		let imgs = await Promise.all(
			items.map(async (element) => {
				let resp = await lib.getjson(`api/find?Telcos:device_product_json.product_type=Mobile Wi-Fi&common_name=${element}&limit=1`);
				return resp[0].merchant_thumb_url;
			})
		);
		return imgs;
	}

	$: {
		filterSearchResults(searchTerm);

		if (selections.merchant_name && selections.brand_name) {
			// filterSearchResults(searchTerm);
			window.location.href = `compare?${lib.qstringify(selections)}`;
		}
		if (selections.common_name) {
			lib.goto(`compare?${lib.qstringify(selections)}`);
		}
	}

	// [ "Three", "Vodafone", "iD Mobile" ] url pattern /img/networks/
	let telcologomap = {
		Three: 'img/networks/three.png',
		Vodafone: 'img/networks/vodafone.png',
		'iD Mobile': 'img/networks/idmobiles.png',
		Virgin: 'img/networks/virgin.png'
	};

	async function filterSearchResults(value) {
		filteredResults = commonNames.filter((commonName) => commonName.toLowerCase().includes(value.toLowerCase()));
		// updatePopper();
	}

	let button;

	onMount(async () => {
		commonNames = await getCommonNames();
	});
</script>

<div class="container">
	<div class=" mt-3" id="autocomplete-input">
		<div class="input-group input-group-lg mb-2 px-1">
			<button class="btn btn-danger rounded-start-5" type="button" id="button-cancel" on:click={() => (searchTerm = '')}>
				<i class="fas fa-times-circle fa-lg" />
			</button>
			<input type="text" class="form-control shadow-sm" placeholder="Search Model or Brand" data-bs-title="Popover title" bind:value={searchTerm} bind:this={button} />

			<button class="btn btn-primary rounded-end-5 px-lg-5" type="button" id="button-addon2">Search</button>
		</div>
		<div class="row ps-lg-3 ps-3 mb-2" id="#searchResults">
			{#if searchTerm.length > 0}
				{#each filteredResults.slice(0, 25) as result}
					<button
						class="col-auto btn {searchTerm === result ? 'btn-dark' : 'btn-outline-dark'} btn-sm m-1"
						on:click={() => {
							searchTerm = result;
							selections.common_name = result;
						}}>{result}</button
					>
				{/each}
			{/if}
		</div>
	</div>

	<!-- add bootstrap 5 carousel with 3 slides having url img/banners/1,2,3.jpg -->
	<div id="carouselExampleIndicators" class="carousel slide">
		<div class="carousel-indicators">
			<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
			<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
			<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
		</div>
		<div class="carousel-inner rounded-4">
			<div class="carousel-item active">
				<img src="img/banners/1.jpg" class="d-block w-100" alt="..." />
			</div>
			<div class="carousel-item">
				<img src="img/banners/2.jpg" class="d-block w-100" alt="..." />
			</div>
			<div class="carousel-item">
				<img src="img/banners/3.jpg" class="d-block w-100" alt="..." />
			</div>
		</div>
		<button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
			<span class="carousel-control-prev-icon" aria-hidden="true"></span>
			<span class="visually-hidden">Previous</span>
		</button>
		<button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
			<span class="carousel-control-next-icon" aria-hidden="true"></span>
			<span class="visually-hidden">Next</span>
		</button>
	</div>
	<div class="mt-2" id="selections">
		{#if selections && Object.keys(selections).length > 0}
			{#each Object.entries(selections) as [key, value] (key)}
				<!-- create a button group -->
				<div class="btn-group me-2 btn-group-sm">
					<button type="button" class="btn btn-primary">{key}</button>
					<button type="button" class="btn btn-outline-dark">{value}</button>
				</div>
			{/each}
			<!-- clear button -->
			<button class="btn btn-danger btn-sm" on:click={() => (selections = {})}>Clear</button>
		{:else}
			Please select a network and brand to start comparing
		{/if}
	</div>
	<!-- SELECTORS -->
	<div class="row flex-lg-row-reverse d-flex mt-3 gap-3 gap-lg-0 h-100">
		<div class="col my-auto" id="how-to-shop">
			<div class="list-group flex-wrap align-self-baseline">
				<span href="#" class="list-group-item list-group-item-action active bg-danger border-black bg-gradient fw-bold" aria-current="true">
					<i class="fa-duotone fa-store-alt"></i>
					HOW TO SHOP?
				</span>
				<span href="#" class="list-group-item list-group-item-action">Method 1: in the search bar type and select a model name</span>
				<span href="#" class="list-group-item list-group-item-action">Method 2: select Network, Brand, Colour and size Listings section will auto update</span>
				<span href="#" class="list-group-item list-group-item-action">now finally compare the plan in the bottom section</span>
			</div>
		</div>
		{#key [selections['Telcos:network'], selections.brand_name]}
			<div class="col-auto col-lg-8 mb-2">
				<div class="list-group">
					<a
						href="#"
						class="list-group-item text-center list-group-item-action active {selections['Telcos:network'] ? 'bg-success' : 'bg-dark'} border-black bg-gradient fw-bold"
						aria-current="true"
					>
						<i class="fa-duotone fa-store-alt"></i>
						Select Merchant
					</a>
					<div class="list-group-item">
						<div class="row justify-content-center">
							{#each Object.entries(data.merchants) as [name, logo]}
								<button
									class="col-{['Three', 'Vodafone Ltd'].includes(name) ? '2' : '2'} btn"
									on:click={() => {
										selections['merchant_name'] = name;
									}}
								>
									<!-- {name} -->
									<img src={logo} alt="Telco" class="img-fluid p-0 border-0" />
								</button>
							{/each}
						</div>
					</div>
				</div>
			</div>
		{/key}
	</div>
	{#key selections}
		<div class=" mt-3 brand-selector">
			<div class="list-group">
				<a
					href="#"
					class="list-group-item text-center list-group-item-action active {selections['brand_name'] ? 'bg-success' : 'bg-dark'} border-black bg-gradient fw-bold"
					aria-current="true"
				>
					<i class="fas fa-mobile-iphone"></i>
					SELECT BRAND
				</a>
				<div class="list-group-item">
					<div class="row justify-content-center py-2 g-1">
						{#if selections.brand_name}
							<!-- show single -->
							<button class="col-lg-auto col-auto btn mt-lg-2 px-1">
								<img src="img/brands/{selections.brand_name.toLowerCase()}.png" alt="Brand" class="img-fluid rounded shadow-sm p-2 w-100" />
							</button>
						{:else}
							{#await getDistinctBrands(selections) then value}
								{#each value as brand}
									<button class="col-lg-auto col-auto btn mt-lg-2 px-1" on:click={() => (selections.brand_name = brand)}>
										<img src="img/brands/{brand.toLowerCase()}.png" alt="Brand" class="img-fluid rounded shadow-sm p-2 w-100" />
									</button>
								{/each}
							{/await}
						{/if}
					</div>
				</div>
			</div>
		</div>
	{/key}

	<div class="mt-3">
		<!-- list group -->
		<div class="list-group" id="sim">
			<a href="#" class="list-group-item text-center list-group-item-action active bg-dark border-black bg-gradient fw-bold" aria-current="true">
				<i class="fas fa-sim-card"></i>
				SIM Cards
			</a>
			<div class="list-group-item">
				<div class="row justify-content-center">
					{#await getDistinctSimProviders() then value}
						{#each value as obj}
							<a class="col-auto mx-lg-3 btn" href="compare?{lib.qstringify(obj.filters)}">
								<img src={obj.img} alt="" />
							</a>
						{/each}
					{/await}
				</div>
			</div>
		</div>
	</div>
	<!-- broadband models -->
	<div class="mt-3">
		<!-- list group -->
		<div class="list-group">
			<a href="#" class="list-group-item text-center list-group-item-action active bg-dark border-black bg-gradient fw-bold" aria-current="true">
				<i class="fa-duotone fa-router"></i>
				Broadband Models
			</a>
			<div class="list-group-item">
				<div class="row justify-content-center">
					{#await getDistinctBroadbandModels() then value}
						{#each value as img}
							<button class="col-auto mx-lg-3 btn">
								<img src={img} alt="" />
							</button>
						{/each}
					{/await}
				</div>
			</div>
		</div>
	</div>

	<div class="row mt-5">
		<!-- Repeat this block for each product -->
		<div class="col-12 col-md-6 col-lg-4 mb-4">
			<div class="card">
				<img src="img/mobiles/iphone.webp" class="card-img-top" alt="Phone" />
				<div class="card-body">
					<h5 class="card-title">Iphone 15 Models</h5>
					<p class="card-text">Some quick example text to build on the product name and make up the bulk of the card's content.</p>
					<div class="d-flex justify-content-between align-items-center">
						<div class="btn-group">
							<button type="button" class="btn btn-sm btn-outline-secondary">View</button>
							<button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
						</div>
						<small class="text-muted">9 mins ago</small>
					</div>
				</div>
			</div>
		</div>
		<!-- End product block -->
	</div>
</div>

<style>
	.carousel-inner img {
		height: 50vh;
	}
	@media (max-width: 768px) {
		.carousel-inner img {
			height: 25vh;
		}
	}
	.brand-selector img {
		max-width: 128px;
		height: 128px;
	}
	@media (max-width: 768px) {
		.brand-selector img {
			max-width: 64px;
			height: auto;
		}
	}

	:global(.popover) {
		/* assume width of parent */
		max-width: 90%;

		/* --bs-popover-max-width: 100%; */
	}
</style>
