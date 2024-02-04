<script>
	export let label, faIconClass, qAttribute, isMobile;
	import * as lib from '$lib';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import shadowFilters from '$lib/stores/shadowFilters';
	// $: console.log($shadowFilters);
	let distincts = [];

	onMount(async () => {
		distincts = await lib.getjson('api/distinct/' + qAttribute);
		// console.log(lib.qparse($shadowFilters));
	});
</script>

<!-- 

<div class="dropdown me-lg-2">
			<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
				<i class="fas fa-shop"></i>
				Merchants</button
			>
			<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
				<li><a class="dropdown-item" href="#">Action</a></li>
				<li><a class="dropdown-item" href="#">Another action</a></li>
				<li><a class="dropdown-item" href="#">Something else here</a></li>
			</ul>
		</div>

 -->

<div class="dropdown me-lg-2">
	<button class="btn btn-secondary {isMobile ? 'btn-sm me-1' : ''} dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
		<i class={faIconClass}></i>
		{label}
	</button>
	<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
		{#each distincts as item}
			<li>
				<button
					class="dropdown-item"
					on:click={() => {
						if (qAttribute == 'Telcos:network?Telcos:device_product_json.product_type=SIM%20Card') {
							$shadowFilters = { "Telcos:device_product_json.product_type": "SIM Card", ["Telcos:network"]: item };
						} else {
							$shadowFilters = { [qAttribute]: item };
						}
						goto(`/compare?${lib.qstringify($shadowFilters)}`, { invalidateAll: true });
					}}
					type="button">{item}</button
				>
			</li>
		{/each}
	</ul>
</div>
