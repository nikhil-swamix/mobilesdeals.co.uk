<script>
	export let label, faIconClass, qAttribute;
	import * as lib from '$lib';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	let distincts = [];
	onMount(async() => {
		distincts = await lib.getjson('api/distinct/' + qAttribute);
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
	<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
		<i class={faIconClass}></i>
		{label}
	</button>
	<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
		{#each distincts as item}
			<li><a class="dropdown-item" href="/compare?{lib.qstringify({ [qAttribute]: item })}">{item}</a></li>
		{/each}
	</ul>
</div>
