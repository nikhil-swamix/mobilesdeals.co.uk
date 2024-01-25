<script>
	export let cname, shadowFilters;
	import * as helpers from '$lib/helpers';
	let meadowFilters = { ...shadowFilters };
	// $: console.log(cname, filters,shadowFilters);
</script>

{#await helpers.getCommonNameVariety(cname, {...shadowFilters}) then details}
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
							{#each details.colours as colour}
								<button
									class="col-lg-auto col-auto btn mx-1 px-1 btn-sm shadow-sm btn-dark bg-gradient mt-lg-2 {shadowFilters['colour'] == colour ? '' : ''}"
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
						</div>
						<div class="mt-2 pt-2 border-top bor">
							<!-- each sizes -->
							{#each details.sizes as size}
								<button
									class="col-lg-auto col-auto btn mx-1 px-1 btn-sm shadow-sm btn-dark bg-gradient {shadowFilters['Telcos:storage_size'] == size ? '' : ''}"
									on:click={() => {
										shadowFilters['Telcos:storage_size'] = size;
										shadowFilters.common_name = cname;
									}}
								>
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
