<script>
	export let deals = [];
	import DataTable from 'datatables.net-bs5';
	import 'datatables.net-buttons-bs5';
	import 'datatables.net-responsive-bs5';
	import { onMount, onDestroy } from 'svelte';
	let table;

	function calcTotalCost(deal) {
		const totalCost = deal['Telcos:month_cost'] * deal['Telcos:term'] + deal['Telcos:initial_cost'];
		return totalCost.toFixed(2);
	}

	onMount(async () => {
		table = new DataTable('#myTable', {
			// autoWidth: true,
			order: [[1, 'asc']],
			pageLength: 25
		});
	});
	onDestroy(() => {
		table?.destroy();
	});
	function calcDataSort(deal) {
		// deal['Telcos:tariff'] has integers and sometimes unlimited, we need to assign 999 to unlimited and integer to integer
		// try using regex and parseint
		let is_unlimited = deal['Telcos:tariff'].toLowerCase().includes('unlimited');
		let int = parseInt(deal['Telcos:tariff'].replace(/[^0-9]/g, ''));
		// console.log(deal['Telcos:tariff'], is_unlimited, int);
		if (is_unlimited) {
			return 999;
		} else if (int) {
			return int;
		} else {
			return 0;
		}
	}
</script>

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
		{#each deals as deal}
			<tr class=" ">
				<td class="col p-1">
					<img src={deal['Telcos:deal_retailer_json']['logo_url']} class="img-fluid" alt="..." />
				</td>
				<td class="">
					<button type="button" class="btn btn-outline-dark btn-sm fw-bold">
						<i class="fa-duotone fa-pound-sign"></i>
						{deal['Telcos:month_cost'] || deal['Telcos:deal_cost_json']['monthly_total_inc_vat']}
					</button>
				</td>
				<td class="px-0">
					<i class="fa-duotone fa-pound-sign"></i>
					{deal['Telcos:initial_cost']}
				</td>
				<td class="px-0">
					<button type="button" class="btn btn-outline-dark btn-sm fw-bold">
						<i class="fa-duotone fa-pound-sign"></i>
						{calcTotalCost(deal)}
					</button>
				</td>
				<td class="px-0">
					<div class="btn-group btn-group-sm" role="group">
						<button type="button" class="btn btn-dark fw-normal px-0" title="Contract Duration">
							<i class="fa-duotone fa-fw fa-timer"></i>
						</button>
						<button type="button" class="btn btn-outline-dark">
							{deal['Telcos:term']} Mo
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
				<td class="px-0" data-sort={calcDataSort(deal)}>
					<div class="btn-group btn-group-sm" role="group">
						<button type="button" class="btn btn-dark fw-normal">
							{deal['Telcos:connectivity'].replace(/ /g, '')}
						</button>
						<button type="button" class="btn btn-outline-dark">
							{deal['Telcos:tariff']}
						</button>
					</div>
				</td>
				<td class="px-0 py-0">
					<a class="btn btn-success" href="deal?_id={deal._id}" target="_blank">
						View Deal <i class="fa-duotone fa-cart-shopping-fast"></i>
					</a>
					{#if deal['Telcos:deal_type_json']['deal_type_name'] == 'Consumer - Affiliate Price'}
						<!-- content here -->
						<i class="fa-duotone fa-gift"></i>
					{/if}
				</td>
			</tr>
		{/each}
	</tbody>
</table>

<style>
	table img {
		max-height: 3em;
	}
	td {
		vertical-align: middle;
	}
</style>
