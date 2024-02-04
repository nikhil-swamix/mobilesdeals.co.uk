<script>
	import DistinctDropdown from './DistinctDropdown.svelte';

	let outerWidth = 768;
	let isMobile = false;
	$: {
		isMobile = outerWidth < 768;
		// console.log(isMobile);
	}
</script>

<svelte:window bind:outerWidth />
<nav class="navbar navbar-expand-lg navbar-dark bg-dark py-1 px-lg-5 fade-in">
	<a class="navbar-brand d-flex align-items-center" href="/">
		<img src="/favicon.png" alt="" height="48" class="rounded me-lg-2" />
		<span class="lead"><i class="fa-duotone fa-mobile-alt px-2"></i>Cheapest Mobile Deals </span>
	</a>

	<div class="d-flex ms-auto flex-wrap">
		<DistinctDropdown {isMobile} label="Merchants" faIconClass="fas fa-shop" qAttribute="merchant_name" />
		<DistinctDropdown {isMobile} label="Networks" faIconClass="fa-duotone fa-diagram-project" qAttribute="Telcos:network" />
		<DistinctDropdown {isMobile} label="Brands" faIconClass="fas fa-bolt" qAttribute="brand_name" />
		<DistinctDropdown {isMobile} label="Sims" faIconClass="fa-duotone fa-sim-cards" qAttribute="Telcos:network?Telcos:device_product_json.product_type=SIM%20Card" />
		<!-- <a class="nav-link" href="#"><i class="fas fa-question-circle"></i> Help</a> -->
		<button type="button" class="btn btn-outline-secondary {isMobile ? 'btn-sm me-1 mt-1' : ''}" data-bs-toggle="modal" data-bs-target="#modalId">
			<i class="fas fa-question-circle"></i> Help
		</button>
	</div>
</nav>
<div class="modal fade mx-0" id="modalId" tabindex="-1" data-bs-keyboard="false" role="dialog" aria-labelledby="modalTitleId" aria-hidden="true">
	<div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-sm" role="document">
		<div class="modal-content">
			<div class="modal-body p-0">
				<div class="col my-auto" id="how-to-shop">
					<div class="list-group flex-wrap align-self-baseline">
						<span href="#" class="list-group-item list-group-item-action active bg-danger border-black bg-gradient fw-bold" aria-current="true">
							<i class="fa-duotone fa-store-alt"></i>
							HOW TO SHOP?
						</span>
						<span href="#" class="list-group-item list-group-item-action">Method 1: in the search bar type and select a model name</span>
						<span href="#" class="list-group-item list-group-item-action">Method 2: from menu select Network,Merchant, Brand, Colour and compare</span>
						<span href="#" class="list-group-item list-group-item-action">now finally compare the plan in the bottom section</span>
					</div>
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal"> Close </button>
				<button type="button" class="btn btn-primary">Save</button>
			</div>
		</div>
	</div>
</div>

<slot />

<footer class="bg-dark text-white text-center p-3">
	<p>MobilesDeals.co.uk All rights reserved &copy; 2023</p>
</footer>

<style>
	.fade-in{
		animation: fadeInAnimation ease 1s;
	}
	@keyframes fadeInAnimation {
		0% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}
</style>
