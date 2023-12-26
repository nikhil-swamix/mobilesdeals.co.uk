<script>
	import { onMount } from 'svelte';
	import * as lib from '$lib';
	import * as helpers from '$lib/helpers';

	let page = lib.page;
	let filters = lib.qparse($page.url);
	let shadowFilters = filters;
	$: {
		console.log(lib.qstringify(shadowFilters));
	}
</script>

<div class="row p-lg-4 mx-lg-5 mx-0">
	<div class="col-12 row mt-2 mt-lg-0" id="filters">
		{#if shadowFilters && Object.keys(shadowFilters).length > 0}
			<div class="col-auto p-lg-1 d-flex align-items-center">You have selected:</div>
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
	<div class="row col-12 ps-3 ps-lg-0 mx-auto">
		{#await helpers.getCommonNames({ ...filters }) then value}
			{#each value as cname}
				{#await helpers.getCommonNameVariety(cname, { ...filters }) then details}
					<div class="col-xxl-3 col-lg-4 col-12 mt-3 mt-xxl-2 p-xxl-2 p-1">
						<button class="card h-100 border-black btn text-start shadow-sm" on:click={() => (shadowFilters.common_name = cname)}>
							<div class="row g-0 h-100 mx-0">
								<div class="col-md-4 col-2 d-flex align-items-center p-0">
									<img src={details.img} class="card-img img-fluid" alt="..." />
								</div>
								<div class="col-md-8 col-10">
									<div class="card-body p-2 px-3 ps-0 g-1">
										<h5 class="card-title fw-bold">{cname}</h5>

										<div class="pt-0">
											<!-- content here -->
											{#if !shadowFilters?.colour}
												{#each details.colours as colour}
													<button
														class="col-lg-auto col-auto btn mx-1 px-1 btn-sm shadow-sm btn-dark bg-gradient mt-lg-2"
														on:click={() => {
															shadowFilters.colour = colour;
															shadowFilters.common_name = cname;
														}}
													>
														<!-- fa -->
														<i class="fas fa-circle fa-lg" style="color: {helpers.colormap[colour]};" />
														{colour}
													</button>
												{/each}
											{/if}
										</div>
										<div class="mt-2 pt-2 border-top bor">
											<!-- each sizes -->
											{#each details.sizes as size}
												<button class="col-lg-auto col-auto btn mx-1 px-1 btn-sm shadow-sm btn-dark bg-gradient" on:click={() => (shadowFilters['Telcos:storage_size'] = size)}>
													{size}
												</button>
											{/each}
										</div>
										<div class="desc pt-2" title={details.desc}>
											{details.desc.replace(cname, '').slice(0, 120)}...
										</div>
									</div>
								</div>
							</div>
						</button>
					</div>
				{/await}
			{/each}
		{/await}
	</div>
</div>

<!-- {filters} -->

<style>
	.card-img {
		transform: scale(1.1);
		margin-left: -1em;
		/* width: 90%; */
		/* width: a; */
	}
	.card-title {
		letter-spacing: -0.05em;
		min-height: 2em;
	}
	.desc {
		font-size: 0.75em;
		line-height: 1.1em;
		/* truncate */
		text-align: justify;
	}
	.card button {
		font-size: 0.75em;
	}
</style>
